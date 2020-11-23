import soundfile as sf
import json
from .fx_settings import FxSettings


class Track(object):
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''

    _samples: int
    _samplerate: int
    _file_name: str
    _beats: int
    _ms_length: float
    _bpm: float
    _fx: FxSettings

    def __init__(self, file_name, beats=None, fx=None):
        file = sf.SoundFile(file_name)
        self._samples = len(file)
        self._samplerate = file.samplerate
        self._file_name = file_name
        self._beats: int = beats
        self._ms_length: float = self.samples / self.samplerate * 1000
        if self._ms_length != 0 and self.beats is not None:
            self._bpm: float = self.beats / self._ms_length * 60000
        else:
            self._bpm = None
        if fx:
            self._fx = fx
        else:
            self._fx = FxSettings()

    def to_dict(self):
        data = {}
        data['__type__'] = 'Track'
        data['beats'] = self.beats
        data['bpm'] = self.bpm
        data['file_name'] = self.file_name
        data['ms_length'] = self.ms_length
        data['samples'] = self.samples
        data['samplerate'] = self.samplerate
        data['fx'] = self.fx
        return data

    def from_dict(self, data):
        self.beats = data['beats']
        self.bpm = data['bpm']
        self.file_name = data['file_name']
        self.ms_length = data['ms_length']
        self.samples = data['samples']
        self.samplerate = data['samplerate']
        self.fx = data['fx']

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, val):
        self._file_name = val

    @property
    def samples(self):
        return self._samples

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, val):
        self._bpm = val

    @property
    def beats(self):
        return self._beats

    @beats.setter
    def beats(self, val):
        self._beats = val

    @property
    def ms_length(self):
        return self._ms_length

    @ms_length.setter
    def ms_length(self, val):
        self._ms_length = val

    @property
    def fx(self):
        return self._fx

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)
