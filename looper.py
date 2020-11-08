import os
# import ntpath
# import sys
# import argparse
# import tempfile
# import queue
# import json

from bullet import Bullet
from transitions import Machine
from data_models.fx_settings import FxSettings
from data_models.loop import Loop
# from data_models.track import Track


class Looper(Machine):
    """An implementation of a Finite State Machine

    The Looper may be in any one of these states at a given time.
      States:
      idle:                   The looper has no audio tracks added
      loaded:                 The looper has at least one track loaded, audio cursor at 0
      playing:                The looper is playing the track list
      recording:              The looper is recording an audio stream
      playing_and_recording:  The looper is playing the track list and recording an audio stream
      paused:                 The audio looper has at least one track loaded, audio cursor is at some other point than 0
    """
    states = ['idle', 'loaded', 'playing',
              'recording', 'playing_and_recording', 'paused']

    transitions = [
        # idle state transitions
        {'trigger': 'load_loop', 'source': 'idle',
         'dest': 'loaded', 'after': 'load_loop'},
        {'trigger': 'add_track', 'source': 'idle',
         'dest': 'loaded', 'after': 'load_track'},
        {'trigger': 'record', 'source': 'idle', 'dest': 'recording'},
        {'trigger': 'metronome', 'source': 'idle',
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': 'idle',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'idle',
         'dest': 'None'},  # Not a transition

        # loaded state transitions
        {'trigger': 'record', 'source': 'loaded',
         'dest': 'playing_and_recording'},
        {'trigger': 'add_track', 'source': 'loaded',
         'dest': '=', 'after': 'load_track'},
        {'trigger': 'remove_track', 'source': 'loaded', 'dest': 'idle',
         'after': 'unload_track', 'conditions': 'no_tracks'},
        {'trigger': 'remove_track', 'source': 'loaded',
         'dest': '=', 'after': 'unload_track'},
        {'trigger': 'record', 'source': 'loaded',
         'dest': 'playing_and_recording'},
        {'trigger': 'play', 'source': 'loaded', 'dest': 'playing'},
        {'trigger': 'metronome', 'source': 'loaded',
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': 'loaded',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'loaded',
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': 'loaded',
         'dest': 'None'},  # Not a transition

        # recording state transitions
        {'trigger': 'record', 'source': 'recording', 'dest': 'playing'},
        {'trigger': 'play', 'source': 'recording', 'dest': 'playing'},
        {'trigger': 'pause', 'source': 'recording', 'dest': 'paused'},
        {'trigger': 'stop', 'source': 'recording', 'dest': 'loaded'},
        {'trigger': 'metronome', 'source': 'recording',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'recording',
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': 'recording',
         'dest': 'None'},  # Not a transition

        # playing state transitions
        {'trigger': 'record', 'source': 'playing',
         'dest': 'playing_and_recording'},
        {'trigger': 'pause', 'source': 'playing', 'dest': 'paused'},
        {'trigger': 'stop', 'source': 'playing', 'dest': 'loaded'},
        {'trigger': 'metronome', 'source': 'playing',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'playing',
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': 'playing',
         'dest': 'None'},  # Not a transition

        # playing_and_recording state transitions
        {'trigger': 'record', 'source': 'playing_and_recording', 'dest': 'playing'},
        {'trigger': 'play', 'source': 'playing_and_recording', 'dest': 'playing'},
        {'trigger': 'pause', 'source': 'playing_and_recording', 'dest': 'paused'},
        {'trigger': 'stop', 'source': 'playing_and_recording', 'dest': 'loaded'},
        {'trigger': 'metronome', 'source': 'playing_and_recording',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'playing_and_recording',
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': 'playing_and_recording',
         'dest': 'None'},  # Not a transition

        # paused state transitions
        {'trigger': 'record', 'source': 'paused',
         'dest': 'playing_and_recording'},
        {'trigger': 'play', 'source': 'paused', 'dest': 'playing'},
        {'trigger': 'pause', 'source': 'paused', 'dest': 'playing'},
        {'trigger': 'stop', 'source': 'paused', 'dest': 'loaded'},
        {'trigger': 'metronome', 'source': 'paused',
         'dest': 'None'},  # Not a transition
        {'trigger': 'metronome_settings', 'source': 'paused',
         'dest': 'None'},  # Not a transition
        {'trigger': 'global_fx', 'source': 'paused',
         'dest': 'None'},  # Not a transition
        {'trigger': 'track_fx', 'source': 'paused',
         'dest': 'None'},  # Not a transition
    ]

    def __init__(self, volume=1, pan=0.5, loop=None):
        Machine.__init__(self, states=self.states, initial='idle')
        self.fx = FxSettings()
        self.machine = Machine(model=self, states=Looper.states, initial='idle',
                               transitions=Looper.transitions, ignore_invalid_triggers=True)
        if(loop == None):
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
        # TODO - write code to unload a track from a loop--should call a method from Loop object
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

        Used at the end of recording in recording or playing_and_recording states
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
        if(self.loop.track_count == 0):
            return True
        return False


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
