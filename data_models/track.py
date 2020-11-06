from dataclasses import dataclass
from fx_settings import FxSettings

@dataclass
class Track:
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''
    filename: str
    bpm: int
    length_in_beats: int
    length_in_ms: int
    fx: FxSettings
