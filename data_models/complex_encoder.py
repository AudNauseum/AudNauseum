import json

#code citation: https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
class ComplexEncoder(json.JSONEncoder):
    """Returns a JSON representation of a complex object
     
    Handles nested JSON of other objects appropriately"""
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)  
