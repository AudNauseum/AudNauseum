import json

# code citation:
# https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json


class ComplexEncoder(json.JSONEncoder):
    """Returns a JSON representation of a complex object

    Handles nested JSON of other objects appropriately"""

    def default(self, obj):
        # print(type(obj))
        if isinstance(obj, list):
            output = []
            for each in obj:
                if hasattr(each, 'to_dict'):
                    output.append(each.to_dict())
            return output
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(obj)
