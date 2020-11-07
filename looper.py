import os
from os import path
from transitions import Machine
from data_models.fx_settings import FxSettings
from data_models.loop import Loop
from data_models.track import Track 

class Looper(Machine):
  states = ['idle', 'loaded', 'playing', 'recording', 'playing_and_recording', 'paused']
  '''
  States:
    idle:                   The looper has no audio tracks added
    loaded:                 The looper has at least one track loaded, audio cursor at 0
    playing:                The looper is playing the track list
    recording:              The looper is recording an audio stream 
    playing_and_recording:  The looper is playing the track list and recording an audio stream
    paused:                 The audio looper has at least one track loaded, audio cursor is at some other point than 0
  '''
  
  transitions = [
    #idle state transitions
    { 'trigger': 'add_track', 'source': 'idle', 'dest': 'loaded' },
    { 'trigger': 'record', 'source': 'idle', 'dest': 'recording' },

    #loaded state transitions
    { 'trigger': 'record', 'source': 'loaded', 'dest': 'playing_and_recording' },
    { 'trigger': 'add_track', 'source': 'loaded', 'dest': '=', 'after': 'load_track' },
    { 'trigger': 'remove_track', 'source': 'loaded', 'dest': 'idle', 'after': 'unload_track', 'conditions' : 'no_tracks' },
    { 'trigger': 'remove_track', 'source': 'loaded', 'dest': '=', 'after': 'unload_track' },
    { 'trigger': 'record', 'source': 'loaded', 'dest': 'playing_and_recording' },
    { 'trigger': 'play', 'source': 'loaded', 'dest': 'playing' },

    #recording state transitions
    { 'trigger': 'record', 'source': 'recording', 'dest': 'playing' },
    { 'trigger': 'play', 'source': 'recording', 'dest': 'playing' },
    { 'trigger': 'pause', 'source': 'recording', 'dest': 'paused' },
    { 'trigger': 'stop', 'source': 'recording', 'dest': 'loaded' },

    #playing state transitions
    { 'trigger': 'record', 'source': 'playing', 'dest': 'playing_and_recording' },
    { 'trigger': 'pause', 'source': 'playing', 'dest': 'paused' },
    { 'trigger': 'stop', 'source': 'playing', 'dest': 'loaded' },

    #playing_and_recording state transitions
    { 'trigger': 'record', 'source': 'playing_and_recording', 'dest': 'playing' },
    { 'trigger': 'play', 'source': 'playing_and_recording', 'dest': 'playing' },
    { 'trigger': 'pause', 'source': 'playing_and_recording', 'dest': 'paused' },
    { 'trigger': 'stop', 'source': 'playing_and_recording', 'dest': 'loaded' },

    #paused state transitions
    { 'trigger': 'record', 'source': 'paused', 'dest': 'playing_and_recording' },
    { 'trigger': 'play', 'source': 'paused', 'dest': 'playing' },
    { 'trigger': 'pause', 'source': 'paused', 'dest': 'playing' },
    { 'trigger': 'stop', 'source': 'paused', 'dest': 'loaded' }   
  ]  
  
  def __init__(self, volume=1, pan=0.5, loop=None):
    Machine.__init__(self, states=self.states, initial='idle')
    self.fx = FxSettings()
    self.machine = Machine(model=self, states=Looper.states, initial='idle', transitions=Looper.transitions, ignore_invalid_triggers=True)
    if(loop == None):
      self.loop = Loop()
    else:
      self.loop = loop
  '''load a Track into the looper.  Appends the track to the track_list, reads Track 
  arguments and generates a numpy array that can be used by sounddevices'''
  def load_track(self, file_path):
    #hardcoded True for testing
    return True

  def unload_track(self, file_path):
    #hardcoded True for testing
    return True

  '''Finds the correct point in the numpy arrays of the tracks and plays them.  Should be used in playing and playing_and_recording states'''
  def play_tracks(self, audioCursor):
    pass

  '''writes input audio stream to disk and sends stream to whatever we use to accumulate audio samples for output'''
  def record_input(self):
    pass
  
  '''converts an audio array into a track.  Used at the end of recording in recording or playing_and_recording states'''
  def write_recording_to_track(self, numpyArray):
    pass

  '''returns true if loading a track was successful'''
  @property
  def has_loaded(self):
    #hardcoded True for testing
    return True

  '''returns true if the track_list is empty'''
  @property
  def no_tracks(self):
    #hardcoded True for Testing
    return True

if __name__ == "__main__":
    l = Looper()
    print(f"Initial State: {l.state}")
    l.add_track('file_path')
    print(f"Add Track changed state to {l.state}")
    l.record()
    print(f"Record changed state to {l.state}")
    l.pause()
    print(f"Pause changed state to {l.state}")
    l.play()
    print(f"Play changed state to {l.state}") 
    l.stop()
    print(f"Stop changed state to {l.state}") 
    l.remove_track('asdf')
    print(f"Remove track changed state to {l.state}")