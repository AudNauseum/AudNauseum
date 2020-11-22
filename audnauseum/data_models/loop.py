import json
from typing import List

from .complex_encoder import ComplexEncoder
from .fx_settings import FxSettings
from .track import Track
from audnauseum.metronome.metronome import Metronome


class Loop(object):
    '''Loop is the primary object that gets passed from state to state'''

    _file_path: str
    _met: Metronome
    _fx: FxSettings
    _tracks: List[Track]
    _audio_cursor: int

    def __init__(self, file_path=None, tracks=None, met=None, fx=None,
                 audio_cursor=0):
        self._file_path = file_path
        if tracks is None:
            tracks = []
        self._tracks = tracks  # List of Tracks in the loop
        if met:
            self._met = met  # Initializes a metronome
        else:
            self._met = Metronome()
        # Initializes Volume, Pan, Pitch, Reverse, and Slip settings for a loop
        if fx:
            self._fx = fx
        else:
            self._fx = FxSettings()
        # Sets the audio cursor to point at the beginning of the loop
        self._audio_cursor = audio_cursor

    def to_dict(self):
        data = {}
        data['__type__'] = 'Loop'
        data['file_path'] = self.file_path
        data['tracks'] = self.tracks
        data['met'] = self.met
        data['fx'] = self.fx
        data['audio_cursor'] = self.audio_cursor
        return data

    def from_dict(self, data):
        self.file_path = data['file_path']
        self.tracks = data['tracks']
        self.met = data['met']
        self.fx = data['fx']
        self.audio_cursor = data['audio_cursor']

    def to_json(self):
        return json.dumps(self, cls=ComplexEncoder, indent=4)

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, fn):
        try:
            self._file_path = fn
        except Exception as e:
            print(
                f"An Exception occurred while writing file_name {fn} to a Loop Object, Message: {e}")

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
        except Exception as e:
            print(
                f"Exception while settings tracks in Loop Object, Message: {e}")

    def append(self, val):
        '''Add a track to track list'''
        try:
            self._tracks = self._tracks + [val]
            return True
        except Exception as e:
            print(
                f"Exception while appending Track to tracklist, Message: {e}")
            return False

    '''Add a list of tracks to track list'''

    def extend(self, val):
        try:
            self._tracks = self.tracks.extend(val)
            return True
        except Exception as e:
            print(
                f"Exception while extending tracks attribute of Loop Object, Message: {e}")
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
        if index < len(self.tracks):
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

    @property
    def audio_cursor(self):
        return self._audio_cursor

    @audio_cursor.setter
    def audio_cursor(self, sample):
        try:
            self._audio_cursor = int(sample)
        except Exception as e:
            print(f"An exception occurred while attempting to set the \
                  audio_cursor of a Loop to {sample}, Message: {e}")

    def write_json(self, file_path):
        self.file_path = file_path
        with open(file_path, 'w') as f:
            f.write(json.dumps(self, cls=ComplexEncoder, indent=4))
