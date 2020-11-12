from complex_encoder import ComplexEncoder
from fx_settings import FxSettings
from track import Track
from metronome import Metronome
import ntpath
import json


class Loop:
    '''Loop is the primary object that gets passed from state to state'''

    def __init__(self):
        self._file_name = None
        self._tracks = [Track]  # List of Tracks in the loop
        self._met = Metronome(100, 4)   # Initializes a metronome
        # Initializes Volume, Pan, Pitch, Reverse, and Slip settings for a loop
        self._fx = FxSettings()
        # Sets the audio cursor to point at the beginning of the loop
        self.audio_cursor = 0

    # TEST METHOD
    def solipsize(self):
        '''Just to test that I can reach a loop object.'''
        print("I am a Loop object")

    @property
    def track_count(self):
        return len(self._tracks)

    @property
    def tracks(self):
        return self._tracks

    @tracks.setter
    def tracks(self, track):
        try:
            self._tracks = track
        except Exception:
            pass

    def append(self, val):
        '''Add a track to track list'''
        try:
            self._tracks = self._tracks + [val]
            return True
        except Exception:
            return False

    '''Add a list of tracks to track list'''

    def extend(self, val):
        try:
            self._tracks = self.tracks.extend(val)
            return True
        except Exception:
            return False

    '''Remove a track by file_path. Removes the first instance of a Track with
    a given file_path'''

    def remove(self, file_path):
        for index, track in enumerate(self.tracks):
            if track.file_name == file_path:
                del self.tracks[index]
                return True
        return False

    # NOTE: If anyone thinks of a good reason to return the object
    # instead of tracking success of the operation, we can do that.
    '''Remove a track by index in the tracks list.  Note: Does not return the
    Track removed from the list. I chose to return a bool to report success of
    the operation.'''

    def pop(self, index):
        if(index < len(self.tracks)):
            self.tracks.pop(index)
            return True
        else:
            return False

    @property
    def met(self):
        return self._met

    @property
    def fx(self):
        return self._fx

    def reprJSON(self):
        return dict(tracks=self.tracks, met=self.met, fx=self.fx)

    def write_json(self, file_name):
        '''Creates or overwrites an existing JSON file with all pertinent
        information about a Loop, including Track objects and FxSettings'''
        with open('./json/' + ntpath.splitext(ntpath.basename(file_name))[0] +
                  '.json', 'w+') as f:
            f.write(json.dumps(self, cls=ComplexEncoder))

    # TODO: implement feature to read from JSON file into objects using a
    # Complex Decoder
