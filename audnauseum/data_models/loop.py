from .complex_encoder import ComplexEncoder
from .fx_settings import FxSettings
from .track import Track
from audnauseum.metronome.metronome import Metronome
import json
import ntpath


class Loop:
    '''Loop is the primary object that gets passed from state to state'''

    def __init__(self):
        self.file_name = None
        self._tracks: list[Track] = []  # List of Tracks in the loop
        self._met = Metronome(100, 4)   # Initializes a metronome
        # Initializes Volume, Pan, Pitch, Reverse, and Slip settings for a loop
        self._fx = FxSettings()
        # Sets the audio cursor to point at the beginning of the loop
        self.audio_cursor = 0

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
            print("Exception while settings tracks in Loop Object")

    def append(self, val):
        '''Add a track to track list'''
        try:
            self._tracks = self._tracks + [val]
            return True
        except Exception:
            print("Exception while appending Track to tracklist")
            return False

    '''Add a list of tracks to track list'''

    def extend(self, val):
        try:
            self._tracks = self.tracks.extend(val)
            return True
        except Exception:
            print("Exception while extending tracks attribute of Loop Object.")
            return False

    '''Remove a track by file_path. Removes the first instance of a Track with 
    a given file_path'''

    def remove(self, file_path):
        for index, track in enumerate(self.tracks):
            if track.file_name == file_path:
                del self.tracks[index]
                return True
        return False

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

    def write_json(self, file_path):
        with open(file_path, 'w') as f:
            f.write(json.dumps(self, ComplexEncoder))

    # TODO: implement feature to read from JSON file into objects using a
    # Complex Decoder


if __name__ == "__main__":
    # TESTS
    # Create Loop
    loop = Loop()
    # Create Tracks
    t1 = Track('resources/recordings/Soft_Piano_Music.wav')
    t2 = Track('resources/recordings/Soft_Piano_Music.wav')

    # Add tracks to loop
    loop.append(t1)
    loop.append(t2)

    # print loop details
    print(loop)

    # access the loop's metronome and fx
    print(f'{loop.met}')
    print(f'{loop.fx}')

    # write loop information to ./json/loops
    loop.write_json()

    # remove a track from the loop by file_name
    if loop.remove('resources/recordings/Soft_Piano_Music.wav'):
        print("I removed a thing.")

    print(loop)

    # remove a track from the loop by index
    if loop.pop(0):
        print("I popped a thing.")

    print(loop)
