import soundfile as sf
import json
import ntpath
from .fx_settings import FxSettings
from .complex_encoder import ComplexEncoder


class Track:
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''

    def __init__(self, file_name, length_in_beats=None):
        file = sf.SoundFile(file_name)
        self._samples = len(file)
        self._samplerate = file.samplerate
        self._file_name = file_name
        self._beat_length: int = length_in_beats
        self._ms_length: float = samples / samplerate * 1000
        if(self._ms_length != 0):
            self._bpm: float = length_in_beats / self._ms_length * 60000
        else:
            self._bpm = None
        self._fx = FxSettings()

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

    def reprJSON(self):
        return dict(file_name=self.file_name, bpm=self.bpm,
                    beat_length=self.beat_length, ms_length=self.ms_length,
                    fx=self.fx)


if __name__ == "__main__":
    t = Track('resources/recordings/Soft_Piano_Music.wav', 100, 8)
    print(f'File Name: {t.file_name}')
    print(f'BPM: {t.bpm}')
    print(f'Length In Beats: {t.beat_length}')
    print(f'Length In MS: {t.ms_length}')
    print('\n\n')
    print("FX Properties:")
    print("==============")
    print(f'Volume: {t.fx.volume}')
    print(f'Pan: {t.fx.pan}')
    print(f'Pitch Adjust: {t.fx.pitch_adjust}')
    print(f'Is Reversed: {t.fx.is_reversed}')
    print(f'Slip: {t.fx.slip}')
    print('\n\n')
    t.fx.volume = 0.5
    print(f'Changed Volume to {t.fx.volume}')
    t.fx.slip = 2468372
    print(f'Changed slip to {t.fx.slip}')
    print("JSON DUMP")
    print(json.dumps(t, cls=ComplexEncoder, indent=4))
    t.write_JSON()
