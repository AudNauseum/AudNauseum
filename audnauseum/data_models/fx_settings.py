import json
from .complex_encoder import ComplexEncoder
from dataclasses import dataclass


@dataclass
class FxSettings:
    '''FxSettings are an attribute of both Tracks and Loops.
    Only "_slip" doesn't make sense when applying effects to loops'''
    _volume: float = 1
    _pan: float = 0.5
    _is_reversed: bool = False
    _pitch_adjust: int = 0
    _slip: int = 0

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value

    @property
    def pan(self):
        return self._pan

    @pan.setter
    def pan(self, value):
        self._pan = value

    @property
    def is_reversed(self):
        return self._is_reversed

    @is_reversed.setter
    def is_reversed(self, value):
        self._is_reversed = value

    @property
    def pitch_adjust(self):
        return self._pitch_adjust

    @pitch_adjust.setter
    def pitch_adjust(self, value):
        self._pitch_adjust = value

    @property
    def slip(self):
        return self._slip

    @slip.setter
    def slip(self, value):
        self._slip = value

    def reprJSON(self):
        return dict(volume=self.volume, pan=self.pan,
                    is_reversed=self.is_reversed,
                    pitch_adjust=self.pitch_adjust,
                    slip=self.slip)
