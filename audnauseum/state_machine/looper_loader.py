import json
from audnauseum.state_machine.looper import Looper
from audnauseum.data_models.complex_encoder import ComplexEncoder


class SettingsDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.hook, *args, **kwargs)

    def hook(self, obj):
        if '__type__' not in obj:
            return obj
        type = obj['__type__']

        if type == 'Looper':
            return Looper(input=obj['input'],
                          output=obj['output'],
                          pass_through=obj['pass_through'])


class LooperLoader(object):
    def __init__(self, settings='settings/settings.json'):
        self.settings = settings
        self.looper = Looper()
        self.load_settings()

    def write_settings(self):
        with open(self.settings, 'w') as f:
            f.write(json.dumps(self.looper, cls=ComplexEncoder, indent=4))

    def read_settings(self):
        with open(self.settings, 'r') as f:
            try:
                return f.read()
            except Exception as e:
                print(
                    f'Exception in read_settings of file: {self.settings}\nMessage: {e}')

    def load_settings(self):
        try:
            json_data = self.read_settings()
            self.looper = json.loads(json_data, cls=SettingsDecoder)
            return True
        except Exception as e:
            print(
                f'Exception while loading data from {self.settings}\nMessage: {e}')
            return False
