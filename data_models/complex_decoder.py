import json

# TODO: Finish Decoder implementation.
# Code citation: https://gist.github.com/simonw/7000493


class ComplexDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

        def object_hook(self, obj):
            if '_type' not in obj:
                return obj
            type = obj['_type']
            if type == 'FxSettings':
                return parser.parse(obj['value'])
            if type == 'Track':
                return parser.parse(obj['value'])
            if type == 'Metronome':
                return parser.parse(obj['value'])
        return obj


if __name__ == "__main__":
    data = {
        "name": "Silent Bob",
        "dt": datetime.datetime(2013, 11, 11, 10, 40, 32)
    }

    print json.loads(s, cls=RoundTripDecoder)
