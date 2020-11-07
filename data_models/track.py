from dataclasses import dataclass
import soundfile as sf
import json, ntpath
from fx_settings import FxSettings
from complex_encoder import ComplexEncoder

class Track:
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''
    def __init__(self, file_name, bpm=None, length_in_beats=None):
        f = sf.SoundFile(file_name)
        samples = len(f)
        samplerate = f.samplerate

        self._file_name= file_name
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
    
    def reprJSON(self):
        return dict(file_name=self.file_name, bpm=self.bpm, beat_length=self.beat_length, ms_length=self.ms_length, fx=self.fx)

    ##TODO: rewrite write_JSON to write all loop and track info to a common file.
    def write_JSON(self):
        print(json.dumps(self, cls=ComplexEncoder))  
        with open('./json/tracks/' + ntpath.splitext(ntpath.basename(self.file_name))[0] + '.json', 'w') as f:
            f.write(json.dumps(self, cls=ComplexEncoder))
    
    #TODO: write a read_JSON feature to read specified content of a JSON file into a track or loop


if __name__ == "__main__":
    t = Track(f'resources/recordings/Soft_Piano_Music.wav', 100, 8)
    print(f'File Name: {t.file_name}')
    print(f'BPM: {t.bpm}')
    print(f'Length In Beats: {t.beat_length}')
    print(f'Length In MS: {t.ms_length}')
    print('\n\n')
    print(f"FX Properties:")
    print(f"==============")
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