import json

'''Returns a JSON representation of a complex object, 
by nesting JSON of other objects appropriately'''
#code citation: https://stackoverflow.com/questions/5160077/encoding-nested-python-object-in-json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)  