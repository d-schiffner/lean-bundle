import json

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        else:
            return json.JSONEncoder.default(self, obj)

# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch06s02.html
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
    
    def __getitem__(self, x):
        return self.__dict__[x]
    
    def __contains__(self, x):
        return x in self.__dict__
    
    def __str__(self):
        return json.dumps(self, indent=1, cls=ComplexEncoder)
    
    def items(self):
        return self.__dict__.items()
    
    def toJSON(self):
        return self.__dict__
    
    @staticmethod
    def dumps(obj):
        return json.dumps(obj, cls=ComplexEncoder)