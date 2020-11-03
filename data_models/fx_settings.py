from dataclasses import dataclass


@dataclass
class FxSettings:
    '''FxSettings are an attribute of both Tracks and Loops.
    Only "_slip" doesn't make sense when applying effects to loops'''
    volume: float = 0.5
    pan: float = 0.5
    is_reversed: bool = False
    pitch_adjust: int = 0
    slip: int = 0
