import soundfile as sf
from fx_settings import FxSettings


class Track:
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''

    def __init__(self, file_name, bpm=None, length_in_beats=None):
        f = sf.SoundFile(file_name)
        samples = len(f)
        samplerate = f.samplerate

        self._file_name = file_name
        self._bpm: float = bpm
        self._beat_length: int = length_in_beats
        self._ms_length: float = samples / samplerate * 1000
        self._fx = FxSettings()

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, val):
        self._file_name = val

    @property
    def bpm(self):
        return self._bpm

    @bpm.setter
    def bpm(self, val):
        self._bpm = val

    @property
    def beat_length(self):
        return self._beat_length

    @beat_length.setter
    def beat_length(self, val):
        self._beat_length = val

    @property
    def ms_length(self):
        return self._ms_length

    @ms_length.setter
    def ms_length(self, val):
        self._ms_length

    @property
    def fx(self):
        return self._fx

    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)

    def reprJSON(self):
        return dict(file_name=self.file_name, bpm=self.bpm,
                    beat_length=self.beat_length, ms_length=self.ms_length,
                    fx=self.fx)
