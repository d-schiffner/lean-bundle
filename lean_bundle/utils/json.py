import json

class JSONClassEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'toJSON'):
            return obj.toJSON()
        return json.JSONEncoder.default(self, obj)

# https://www.safaribooksonline.com/library/view/python-cookbook-3rd/9781449357337/ch06s02.html
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
    
    def __getitem__(self, x):
        return self.__dict__[x]
    
    def __setitem__(self, x, v):
        self.__dict__[x] = v

    def __delitem__(self, k):
        del self.__dict__[k]

    def __contains__(self, x):
        return x in self.__dict__
    
    def __str__(self):
        return json.dumps(self, indent=1, cls=JSONClassEncoder)
    
    def items(self):
        return self.__dict__.items()
    
    def toJSON(self):
        return self.__dict__
    
    @staticmethod
    def dumps(*args, **kwargs):
        kwargs['cls'] = JSONClassEncoder
        return json.dumps(*args, **kwargs)
    
    @staticmethod
    def dump(*args, **kwargs):
        kwargs['cls'] = JSONClassEncoder
        return json.dump(*args, **kwargs)
