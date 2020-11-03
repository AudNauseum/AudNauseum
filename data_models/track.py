from dataclasses import dataclass


@dataclass
class Track:
    '''A track represents an audio stream and a set of
    parameters that allow different tracks to sync together'''
    filename: str
    bpm: int
    length_in_beats: int
    length_in_ms: int
    bit_depth: int = 16
    sample_rate: int = 44100
    is_stereo: bool = False
