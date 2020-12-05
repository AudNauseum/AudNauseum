from audnauseum.audio_tools.wav_reader import WavReader
from audnauseum.audio_tools.player import Player
from audnauseum.data_models.loop import Loop
from audnauseum.data_models.track import Track
from audnauseum.data_models.complex_decoder import ComplexDecoder
from audnauseum.audio_tools.recorder import Recorder
from audnauseum.audio_tools.aggregator import Aggregator
from transitions import Machine
import sounddevice as sd
import enum
import json


class LooperStates(enum.Enum):
    '''The list of possible states AudNauseum can be in'''
    IDLE = 0
    LOADED = 1
    PLAYING = 2
    RECORDING = 3
    PLAYING_AND_RECORDING = 4
    PAUSED = 5


class Looper:
    """An implementation of a Finite State Machine

    The Looper may be in any one of these states at a given time.
      States:
      idle:                   The looper has no audio tracks added
      loaded:                 The looper has at least one track loaded,
                                audio cursor at 0
      playing:                The looper is playing the track list
      recording:              The looper is recording an audio stream
      playing_and_recording:  The looper is playing the track list and
                                recording an audio stream
      paused:                 The audio looper has at least one track loaded,
                                audio cursor is at some other point than 0
    """

    # Type Hints
    loop: Loop
    player: Player
    machine: Machine
    recorder: Recorder
    aggregator: Aggregator
    reader: WavReader

    transitions = [
        # idle state transitions
        {'trigger': 'load', 'source': LooperStates.IDLE,
         'dest': LooperStates.LOADED, 'conditions': ['load_loop', 'tracks_exist']},
        {'trigger': 'add_track', 'source': LooperStates.IDLE,
         'dest': LooperStates.LOADED, 'after': 'load_track'},
        {'trigger': 'record', 'source': LooperStates.IDLE,
            'dest': LooperStates.RECORDING, 'after': 'start_recording'},
        {'trigger': 'metronome', 'source': LooperStates.IDLE,
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': LooperStates.IDLE,
         'dest': 'None', 'before': 'toggle_metronome'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.IDLE,
         'dest': 'None'},  # Not a transition

        # loaded state transitions
        {'trigger': 'load', 'source': LooperStates.LOADED,
         'dest': '=', 'conditions': ['load_loop']},
        {'trigger': 'record', 'source': LooperStates.LOADED,
         'dest': LooperStates.PLAYING_AND_RECORDING, 'after': 'start_playing_and_recording'},
        {'trigger': 'add_track', 'source': LooperStates.LOADED,
         'dest': '=', 'after': 'load_track'},
        {'trigger': 'remove_track', 'source': LooperStates.LOADED,
         'dest': LooperStates.IDLE, 'conditions': ['unload_track', 'no_tracks']},
        {'trigger': 'play', 'source': LooperStates.LOADED,
            'dest': LooperStates.PLAYING, 'after': 'play_tracks'},
        {'trigger': 'metronome', 'source': LooperStates.LOADED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': LooperStates.LOADED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.LOADED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.LOADED,
         'dest': 'None'},  # Not a transition

        # recording state transitions
        {'trigger': 'record', 'source': LooperStates.RECORDING,
            'dest': LooperStates.PLAYING, 'before': 'stop_recording', 'after': 'play_tracks'},
        {'trigger': 'play', 'source': LooperStates.RECORDING,
            'dest': LooperStates.PLAYING, 'before': 'stop_recording', 'after': 'play_tracks'},
        {'trigger': 'pause', 'source': LooperStates.RECORDING,
            'dest': LooperStates.PAUSED, 'before': 'stop_recording'},
        {'trigger': 'stop', 'source': LooperStates.RECORDING,
            'dest': LooperStates.LOADED, 'before': 'stop_recording'},
        {'trigger': 'metronome', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition

        # playing state transitions
        {'trigger': 'record', 'source': LooperStates.PLAYING,
         'dest': LooperStates.PLAYING_AND_RECORDING, 'after': 'start_recording'},
        {'trigger': 'add_track', 'source': LooperStates.PLAYING,
         'dest': '=', 'after': 'load_track'},
        {'trigger': 'pause', 'source': LooperStates.PLAYING, 'before': 'stop_playing',
            'dest': LooperStates.PAUSED},
        {'trigger': 'stop', 'source': LooperStates.PLAYING, 'before': 'stop_playing',
            'dest': LooperStates.LOADED},
        {'trigger': 'metronome', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition

        # playing_and_recording state transitions
        {'trigger': 'record', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PLAYING, 'before': 'stop_recording'},
        {'trigger': 'add_track', 'source': LooperStates.PLAYING_AND_RECORDING,
         'dest': '=', 'after': 'load_track'},
        {'trigger': 'play', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PLAYING, 'before': 'stop_recording'},
        {'trigger': 'pause', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PAUSED, 'before': 'stop_playing_and_recording'},
        {'trigger': 'stop', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.LOADED, 'before': 'stop_playing_and_recording'},
        {'trigger': 'metronome', 'source': LooperStates.PLAYING_AND_RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.PLAYING_AND_RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.PLAYING_AND_RECORDING,
         'dest': 'None'},  # Not a transition

        # paused state transitions
        {'trigger': 'record', 'source': LooperStates.PAUSED,
         'dest': LooperStates.PLAYING_AND_RECORDING},
        {'trigger': 'play', 'source': LooperStates.PAUSED,
            'dest': LooperStates.PLAYING, 'after': 'play_tracks'},
        {'trigger': 'pause', 'source': LooperStates.PAUSED,
            'dest': LooperStates.PLAYING, 'after': 'play_tracks'},
        {'trigger': 'stop', 'source': LooperStates.PAUSED,
            'dest': LooperStates.LOADED},
        {'trigger': 'metronome', 'source': LooperStates.PAUSED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': LooperStates.PAUSED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.PAUSED,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.PAUSED,
         'dest': 'None'},  # Not a transition
    ]

    def __init__(self, loop=None):
        self.machine = Machine(model=self, states=LooperStates,
                               initial=LooperStates.IDLE,
                               transitions=Looper.transitions,
                               ignore_invalid_triggers=True,
                               after_state_change=self.echo_state_change)

        self.set_default_channels()

        if loop is None:
            self.loop = Loop()
        else:
            self.loop = loop

        self.recorder = Recorder(loop=self.loop)
        self.player = Player(loop=self.loop)
        self.reader = WavReader(
            loop=self.loop, last_block_notifier_queue=self.player.last_block_notifier_queue)
        self.aggregator = Aggregator(
            loop=self.loop, player_queue=self.player.input_queue, reader=self.reader)

        # Create a default (empty track) loop upon startup & load it
        default_path = './resources/json/default.json'
        self.write_loop(default_path)
        self.load_loop(default_path)

    def set_default_channels(self):
        """Detects and sets the default sounddevice channels

        Checks the Host APIs of the user's OS audio settings for the
        default input and output devices.
        Sets the sounddevice default channels tuple to the capabilities
        of the input and output devices.
        On Linux, the default input/output devices are often a "virtual"
        device using ALSA and can have 32, 64, or even 128 channels. This
        value is clamped to 2 for what the physical device can support.
        """
        for api in sd.query_hostapis():
            input_device = api.get('default_input_device')
            output_device = api.get('default_output_device')
            if input_device is not None and input_device >= 0 \
                    and output_device is not None and output_device >= 0:
                devices = sd.query_devices()
                input_channels = devices[input_device]['max_input_channels']
                if input_channels > 2:
                    # Clamp value in case of virtual device
                    input_channels = 2
                output_channels = devices[output_device]['max_output_channels']
                if output_channels > 2:
                    # Clamp value in case of virtual device
                    output_channels = 2
                sd.default.channels = input_channels, output_channels
                break

    def load_loop(self, file_path: str):
        """Reads a JSON file using the deserializer into a Loop object

        Swaps to a new Loop object given a path to a JSON file. Updates
        mutable references in object variables.
        """
        try:
            json_data = self.read_json(file_path)
            self.loop = json.loads(json_data, cls=ComplexDecoder)
            self.reader.loop = self.loop
            self.aggregator.loop = self.loop
            self.player.loop = self.loop
            return True
        except Exception as e:
            print(f'Exception while loading data from {file_path}')
            print(f'Message: {e}')
            return False

    def write_loop(self, file_path: str):
        if not file_path.lower().endswith(".json"):
            file_path += ".json"
        self.loop.write_json(file_path)

    def read_json(self, file_path: str):
        with open(file_path, 'r') as f:
            try:
                return f.read()
            except Exception as e:
                print(f'Exception in read_json of file: {file_path}')
                print(f'Message: {e}')

    def echo_state_change(self, *args):
        """TEMPORARY: Prints the state to the terminal after changing

        Unknown why at this time, but an argument is passed in when
        a state change is triggered by clicking a UI button but not
        passed in when triggered directly (i.e. in tests).
        """
        print(f'{self.state=}')

    def load_track(self, file_path: str):
        """Load a Track into the looper.

        If the Looper is currently playing, opens the respective file
        handle to start playback for that track.
        """
        # TODO beats are currently hard-coded to be 20 for all new Tracks
        try:
            x = Track(file_path, beats=20)
            self.loop.append(x)
            if self.state == LooperStates.PLAYING or self.state == LooperStates.PLAYING_AND_RECORDING:
                self.aggregator.add_track(file_path)
            return True
        except Exception as e:
            print(
                f'Exception while loading track from {file_path}\nMessage: {e}')
            return False

    def unload_track(self, file_path: str):
        """Remove a Track from the looper.

        If the Looper is currently playing, closes the respective
        file handle to cease playback for that track.
        """
        try:
            self.loop.remove(file_path)
            self.aggregator.remove_track(file_path)
            return True
        except Exception as e:
            print(
                f'Exception while removing track from {file_path}\nMessage: {e}')
            return False

    def play_tracks(self, *args):
        '''Finds the correct point in the numpy arrays of the tracks
        and plays them. Should be used in playing and playing_and_recording
        states.
        '''
        self.aggregator.start()
        self.player.play()

    def stop_playing(self, *args):
        """Stops the current playing output"""
        self.loop.audio_cursor = 0
        if self.aggregator and self.aggregator.is_running:
            self.aggregator.stop()
        if self.player and self.player.playing:
            self.player.stop()

    def start_recording(self, *args):
        '''Writes input audio stream to disk and sends stream to output'''
        self.recorder = Recorder(loop=self.loop)
        self.recorder.on_rec()

    def stop_recording(self, *args):
        '''Creates a Track from recording, appends to loop'''
        if self.recorder and self.recorder.recording:
            track = self.recorder.on_stop()
            self.loop.append(track)

    def start_playing_and_recording(self, *args):
        self.start_recording()
        self.play_tracks()

    def stop_playing_and_recording(self, *args):
        self.stop_playing()
        self.stop_recording()

    @ property
    def has_loaded(self):
        '''Used for conditional transitions where a file must
        successfully be loaded.
        Returns true if loading a track was successful
        '''
        # TODO
        # hardcoded True for testing
        return True

    @ property
    def no_tracks(self):
        '''Used for conditional transitions where a Loop must be empty.
        Returns true if the track_list is empty
        '''
        return len(self.loop.tracks) == 0

    @ property
    def tracks_exist(self):
        '''Used for conditional transitions where a Loop must be empty.
        Returns true if the track_list is empty
        '''
        return len(self.loop.tracks) != 0

    # Metronome controls
    def metronome_toggle(self):
        '''Turn metronome ON and OFF'''
        self.loop.met.is_on = not(self.loop.met.is_on)
        return True

    def metronome_volume_inc(self):
        '''Increase Volume of metronome'''
        if self.loop.met.volume < 1:
            self.loop.met.volume += 0.01
            return True
        return False

    def metronome_volume_dec(self):
        '''Decrease volume of metronome'''
        if self.loop.met.volume > 0:
            self.loop.met.volume -= 1
            return True
        return False

    def metronome_set_bpm(self, bpm):
        if bpm > 0 and bpm < 300:
            self.loop.met.bpm = int(bpm)
            return True
        return False

    def metronome_bpm_inc(self):
        if self.loop.met.bpm < 300:
            self.loop.met.bpm += 1
            return True
        return False

    def metronome_bpm_dec(self):
        if self.loop.met.bpm > 0:
            self.loop.met.bpm -= 1
            return True
        return False

    def metronome_set_beats(self, beats):
        if beats > 0:
            self.loop.met.beats = int(beats)
            return True
        return False

    def metronome_beats_inc(self):
        self.loop.met.beats += 1
        return True

    def metronome_beats_dec(self):
        if self.loop.met.beats > 1:
            self.loop.met.beats -= 1
            return True
        return False

    def metronome_toggle_count_in(self):
        '''Let's call count-in a stretch goal.  It will affect what happens
        where the use presses record, and that might add more complexity than
        we care to.'''
        self.loop.met.count_in = not(self.loop.met.count_in)
        return True

    # Loop Effects controls

    def convert_volume_to_gui(self, loop_scale_volume: float) -> int:
        loop_range = [0., 1]
        gui_range = [0., 100.]
        loop_scale = (loop_range[1] - loop_range[0])
        gui_scale = (gui_range[1] - gui_range[0])
        gui_volume = round((((loop_scale_volume) *
                             gui_scale) / loop_scale) + gui_range[0])
        return gui_volume

    def convert_gui_to_volume(self, gui_scale_volume: int) -> float:
        loop_range = [0.0001, 1.0001]
        gui_range = [0., 100.]
        loop_scale = (loop_range[1] - loop_range[0])
        gui_scale = (gui_range[1] - gui_range[0])
        loop_volume = (((gui_scale_volume) *
                        loop_scale) / gui_scale) + loop_range[0]
        return loop_volume

    def get_volume(self):
        return self.convert_volume_to_gui(self.loop.fx.volume)

    def set_volume(self, gui_volume: int):
        loop_vol = self.convert_gui_to_volume(gui_volume)
        if 0 <= loop_vol <= 1:
            self.loop.fx.volume = loop_vol
            return True
        return False

    def volume_inc(self):
        if self.loop.fx.volume <= 0.99:
            self.loop.fx.volume += 0.01
            return True
        return False

    def volume_dec(self):
        if self.loop.fx.volume >= 0.01:
            self.loop.fx.volume -= 0.01
            return True
        return False

    def set_pan(self, pan):
        if pan >= -1 and pan <= 1:
            self.loop.fx.pitch_adjust = pan
            return True
        return False

    def pan_inc(self):
        if self.loop.fx.pan <= 0.99:
            self.loop.fx.pan += 0.01
            return True
        return False

    def pan_dec(self):
        if self.loop.fx.pan >= -0.99:
            self.loop.fx.pan -= 0.01
            return True
        return False

    # Track controls
    def track_get_volume(self, track: Track):
        return self.convert_volume_to_gui(track.fx.volume)

    def track_set_volume(self, track: Track, gui_volume: int):
        track_volume = self.convert_gui_to_volume(gui_volume)
        if 0. <= track_volume <= 1.0001:
            track.fx.volume = track_volume
            return True
        return False

    def track_volume_inc(self, track):
        if track.fx.volume <= 0.99:
            track.fx.volume += 0.01
            return True
        return False

    def track_volume_dec(self, track):
        if track.fx.volume >= 0.01:
            track.fx.volume -= 0.01
            return True
        return False

    def track_set_pan(self, track, pan):
        if pan >= 0 and pan <= 1:
            track.fx.pan = pan
            return True
        return False

    def track_toggle_reverse(self, track):
        track.fx.is_reversed = not(track.fx.is_reversed)

    def track_set_pitch_adjust(self, track, adjust):
        track.fx.pitch_adjust = adjust

    def track_pitch_adjust_inc(self, track):
        track.fx.pitch_adjust += 1

    def track_pitch_adjust_dec(self, track):
        track.fx.pitch_adjust -= 1

    def track_set_slip(self, track, slip_ms):
        slip_ms %= track.ms_length
        track.fx.slip = track.samples / track.samplerate * slip_ms

    def track_slip_inc(self, track):
        '''increments by 1 ms'''
        if int(track.fx.slip + track.samplerate/1000) < track.samples:
            track.fx.slip += track.samplerate/1000
        else:
            track.fx.slip = 0  # We hit the end of the file, so start over
        return True

    def track_slip_dec(self, track):
        '''decrements by 1 ms'''
        if int(track.fx.slip - track.samplerate/1000) > 0:
            track.fx.slip -= track.samplerate/1000
        else:
            track.fx.slip = track.samples - track.samplerate/1000
            # We slipped back from the beginning of the file, so go to end, and
            # back up 1ms
        return True

    def shut_down(self, event):
        """Closes open resources before shutting down the GUI.

        Called by the PyQt5 closeEvent, passes the PyQt5.QtGui.QCloseEvent
        object as an argument but is unneeded."""
        print('Shutting down AudNauseum...')

        self.stop_playing_and_recording()

        print('Goodbye!')

    def get_track_list(self):
        return self.loop.tracks

    def get_last_recording(self):
        return self.loop.tracks[-1].file_path
