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
         'dest': 'None'},  # Not a transition
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
        '''Finds the correct point in the numpy arrays of the tracks and plays them.

        Should be used in playing and playing_and_recording states.
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
        '''Used for conditional transitions where a file must successfully be loaded.

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
