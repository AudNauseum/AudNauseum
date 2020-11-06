from metronome.metronome import Metronome
from data_models.track import Track
from data_models.fx_settings import FxSettings


class Loop:
    '''Loop is the primary object that gets passed from state to state'''

    def __init__(self):
        self.tracks: list[Track] = []  # List of Tracks in the loop
        self.met = Metronome(100, 4)
        self.fx = FxSettings()

    def addTrack(self, track: Track):
        self.tracks.append(track)

    def removeTrack(self, track: Track):
        self.tracks.remove(track)
    
    def solipsize(self):
        print(f"I am a Loop object")
    
    @property
    def track_count(self):
        return len(self.tracks)
