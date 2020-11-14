from audnauseum.data_models.loop import Loop
from audnauseum.data_models.fx_settings import FxSettings
from transitions import Machine
from bullet import Bullet
import os
import enum

# import ntpath

# import argparse
# import tempfile
# import queue
# import json


# from data_models.track import Track


class LooperStates(enum.Enum):
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

    transitions = [
        # idle state transitions
        {'trigger': 'load_loop', 'source': LooperStates.IDLE,
         'dest': LooperStates.LOADED, 'after': 'load_loop'},
        {'trigger': 'add_track', 'source': LooperStates.IDLE,
         'dest': LooperStates.LOADED, 'after': 'load_track'},
        {'trigger': 'record', 'source': LooperStates.IDLE,
            'dest': LooperStates.RECORDING},
        {'trigger': 'metronome', 'source': LooperStates.IDLE,
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': LooperStates.IDLE,
         'dest': 'None', 'before': 'toggle_metronome'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.IDLE,
         'dest': 'None'},  # Not a transition

        # loaded state transitions
        {'trigger': 'record', 'source': LooperStates.LOADED,
         'dest': LooperStates.PLAYING_AND_RECORDING},
        {'trigger': 'add_track', 'source': LooperStates.LOADED,
         'dest': '=', 'after': 'load_track'},
        {'trigger': 'remove_track', 'source': LooperStates.LOADED,
         'dest': LooperStates.IDLE, 'after': 'unload_track',
         'conditions': 'no_tracks'},
        {'trigger': 'remove_track', 'source': LooperStates.LOADED,
         'dest': '=', 'after': 'unload_track'},
        {'trigger': 'record', 'source': LooperStates.LOADED,
         'dest': LooperStates.PLAYING_AND_RECORDING},
        {'trigger': 'play', 'source': LooperStates.LOADED,
            'dest': LooperStates.PLAYING},
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
            'dest': LooperStates.PLAYING},
        {'trigger': 'play', 'source': LooperStates.RECORDING,
            'dest': LooperStates.PLAYING},
        {'trigger': 'pause', 'source': LooperStates.RECORDING,
            'dest': LooperStates.PAUSED},
        {'trigger': 'stop', 'source': LooperStates.RECORDING,
            'dest': LooperStates.LOADED},
        {'trigger': 'metronome', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.RECORDING,
         'dest': 'None'},  # Not a transition

        # playing state transitions
        {'trigger': 'record', 'source': LooperStates.PLAYING,
         'dest': LooperStates.PLAYING_AND_RECORDING},
        {'trigger': 'pause', 'source': LooperStates.PLAYING,
            'dest': LooperStates.PAUSED},
        {'trigger': 'stop', 'source': LooperStates.PLAYING,
            'dest': LooperStates.LOADED},
        {'trigger': 'metronome', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': LooperStates.PLAYING,
         'dest': 'None'},  # Not a transition

        # playing_and_recording state transitions
        {'trigger': 'record', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PLAYING},
        {'trigger': 'play', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PLAYING},
        {'trigger': 'pause', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.PAUSED},
        {'trigger': 'stop', 'source': LooperStates.PLAYING_AND_RECORDING,
            'dest': LooperStates.LOADED},
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
            'dest': LooperStates.PLAYING},
        {'trigger': 'pause', 'source': LooperStates.PAUSED,
            'dest': LooperStates.PLAYING},
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

    def __init__(self, volume=1, pan=0.5, loop=None):
        self.fx = FxSettings()
        self.machine = Machine(model=self, states=LooperStates,
                               initial=LooperStates.IDLE,
                               transitions=Looper.transitions,
                               ignore_invalid_triggers=True)
        if loop is None:
            self.loop = Loop()
        else:
            self.loop = loop

    def load_loop(self):
        # TODO
        pass

    def select_track(self):
        """Displays a list of audio files to import"""
        tracks = list(os.listdir('resources/recordings'))
        if tracks:
            cli = Bullet(prompt='Choose a Track:', choices=tracks)
            track = cli.launch()
            return track

    def load_track(self):
        '''Load a Track into the looper.

        Appends the track to the track_list, reads Track
        arguments and generates a numpy array that can be used by sounddevices.
        '''
        # TODO
        pass

    def unload_track(self):
        # TODO - write code to unload a track from a loop
        # should call a method from Loop object
        # hardcoded True for testing
        return True

    def play_tracks(self, audioCursor):
        '''Finds the correct point in the numpy arrays of the tracks 
        and plays them. Should be used in playing and playing_and_recording 
        states.
        '''
        # TODO-DAVE
        pass

    def record_input(self):
        '''Writes input audio stream to disk and sends stream to output'''
        # TODO-STEVE
        pass

    def write_recording_to_track(self, numpyArray):
        '''Converts an audio array into a track.
        Used at the end of recording in recording or playing_and_recording
        '''
        pass

    @property
    def has_loaded(self):
        '''Used for conditional transitions where a file must 
        successfully be loaded.
        Returns true if loading a track was successful
        '''
        # TODO
        # hardcoded True for testing
        return True

    @property
    def no_tracks(self):
        '''Used for conditional transitions where a Loop must be empty.
        Returns true if the track_list is empty
        '''
        return self.loop.track_count == 0

    # Metronome controls
    def metronome_toggle(self):
        '''Turn metronome ON and OFF'''
        self.loop.met.is_on = not(self.loop.met.is_on)
        return True

    def metronome_volume_inc(self):
        '''Increase Volume of metronome'''
        if(self.loop.met.volume < 1):
            self.loop.met.volume += 0.01
            return True
        return False

    def metronome_volume_dec(self):
        '''Decrease volume of metronome'''
        if(self.loop.met.volume > 0):
            self.loop.met.volume -= 1
            return True
        return False

    def metronome_set_bpm(self, bpm):
        if(bpm > 0 and bpm < 300):
            self.loop.met.bpm = int(bpm)
            return True
        return False

    def metronome_bpm_inc(self):
        if(bpm < 300):
            self.loop.met.bpm += 1
            return True
        return False

    def metronome_bpm_dec(self):
        if(bpm > 0):
            self.loop.met.bpm -= 1
            return True
        return False

    def metronome_set_beats(self, beats):
        if(beats > 0):
            self.loop.met.beats = int(beats)
            return True
        return False

    def metronome_beats_inc(self):
        self.loop.met.beats += 1
        return True

    def metronome_beats_dec(self):
        if(self.loop.met.beats > 1):
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
    def set_volume(self, volume):
        if(volume >= 0 and volume <= 1):
            self.loop.fx.volume = volume
            return True
        return False

    def volume_inc(self):
        if(self.loop.fx.volume <= 0.99):
            self.loop.fx.volume += 0.01
            return True
        return False

    def volume_dec(self):
        if(self.loop.fx.volume >= 0.01):
            self.loop.fx.volume -= 0.01
            return True
        return False

    def set_pan(self, pan):
        if(pan >= 0 and pan <= 1):
            self.loop.fx.pitch_adjust = pan
            return True
        return False

    def pan_inc(self):
        if(self.loop.fx.pan <= 0.99):
            self.loop.fx.pan += 0.01
            return True
        return False

    def pan_dec(self):
        if(self.loop.fx.pan >= 0.01):
            self.loop.fx.pan -= 0.01
            return True
        return False

    # Track controls
    def create_track(self, audio_file):
        t = Track(audio_file)
        return t

    def add_track(self, track):
        self.loop.append(track)

    def set_track_beat_length(self, track, beat_length):
        track.beat_length = beat_length

    def calc_track_bpm(self, track):
        track.bpm = track.beat_length/track.ms_length * 60000

    def track_set_volume(self, track, volume):
        if(volume >= 0 and volume <= 1):
            track.fx.volume = volume
            return True
        return False

    def track_volume_inc(self, track):
        if(track.fx.volume <= 0.99):
            track.fx.volume += 0.01
            return True
        return False

    def track_volume_dec(self, track):
        if(track.fx.volume >= 0.01):
            track.fx.volume -= 0.01
            return True
        return False

    def track_set_pan(self, track, pan):
        if(pan >= 0 and pan <= 1):
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
        if(int((track.fx.slip + track.samplerate/1000)) < track.samples):
            track.fx.slip += track.samplerate/1000
        else:
            track.fx.slip = 0  # We hit the end of the file, so start over
        return True

    def track_slip_dec(self, track):
        '''decriments by 1 ms'''
        if(int((track.fx.slip - track.samplerate/1000)) > 0):
            track.fx.slip -= track.samplerate/1000
        else:
            track.fx.slip = track.samples - track.samplerate/1000
            # We slipped back from the beginning of the file, so go to end, and
            # back up 1ms
        return True


if __name__ == "__main__":
    looper = Looper()
    print(f"Initial State: {looper.state}")
    looper.add_track()
    print(f"Add Track changed state to {looper.state}")
    looper.record()
    print(f"Record changed state to {looper.state}")
    looper.pause()
    print(f"Pause changed state to {looper.state}")
    looper.play()
    print(f"Play changed state to {looper.state}")
    looper.stop()
    print(f"Stop changed state to {looper.state}")
    looper.remove_track()
    print(f"Remove track changed state to {looper.state}")
