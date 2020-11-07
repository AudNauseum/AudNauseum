import json

##TODO: Finish Decoder implementation.  
##Code citation: https://gist.github.com/simonw/7000493
class ComplexDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

        def object_hook(self, obj):
            if '_type' not in obj:
                return obj
            type = obj['_type']
            