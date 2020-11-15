import json
from .fx_settings import FxSettings
from .track import Track
from .loop import Loop
from audnauseum.metronome.metronome import Metronome

# TODO: Finish Decoder implementation.
# Code citation: https://gist.github.com/simonw/7000493


class ComplexDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.hook, *args, **kwargs)

    def hook(self, obj):
        if '__type__' not in obj:
            return obj
        type = obj['__type__']
        if type == 'FxSettings':
            return FxSettings(volume=obj['volume'],
                              pan=obj['pan'],
                              is_reversed=obj['is_reversed'],
                              pitch_adjust=obj['pitch_adjust'],
                              slip=obj['slip'])
        if type == 'Metronome':
            return Metronome(bpm=obj['bpm'],
                             beats=obj['beats'],
                             volume=obj['volume'],
                             count_in=obj['count_in'],
                             is_on=obj['is_on']
                             )
        if type == 'Track':
            return Track(file_name=obj['file_name'],
                         beats=obj['beats'],
                         fx=obj['fx'])

        if type == 'Loop':
            return Loop(file_path=obj['file_path'],
                        tracks=obj['tracks'],
                        met=obj['met'],
                        fx=obj['fx'],
                        audio_cursor=obj['audio_cursor'])
