import json


class FxSettings(object):
    '''FxSettings are an attribute of both Tracks and Loops.
    Only "_slip" doesn't make sense when applying effects to loops'''

    def __init__(self, volume=1.0, pan=0.5, is_reversed=False, pitch_adjust=0, slip=0,):
        self._volume = volume
        self._pan = pan
        self._is_reversed = is_reversed
        self._pitch_adjust = pitch_adjust
        self._slip = slip

    def to_dict(self):
        data = {}
        data['__type__'] = 'FxSettings'
        data['volume'] = self.volume
        data['pan'] = self.pan
        data['is_reversed'] = self.is_reversed
        data['pitch_adjust'] = self.pitch_adjust
        data['slip'] = self.slip
        return data

    def from_dict(self, data):
        self.volume = data['volume']
        self.pan = data['pan']
        self.is_reversed = data['is_reversed']
        self.pitch_adjust = data['pitch_adjust']
        self.slip = data['slip']

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

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
