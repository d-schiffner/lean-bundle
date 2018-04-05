from os import path
from .base import LeanBase
from utils.json import JSONObject

class LeanGroup(LeanBase):
    def __init__(self, backend, name):
        super().__init__(backend, name)

    def from_json(self, json, ignore=[]):
        if not hasattr(json, 'items'):
            raise AssertionError("Given json has no items()")
        for k,v in json.items():
            if k in ignore:
                continue
            if type(v) == JSONObject:
                grp = self.create_group(k)
                grp.from_json(v)
            else:
                self.attrs[k] = v
        return self

    def create_group(self, name):
        key = path.join(self.name, name)
        if key in self.backend:
            raise Exception("Key {} already exists".format(key))
        grp = self.backend[key] = LeanGroup(self.backend, key)
        return grp

    def require_group(self, name):
        key = path.abspath(path.join(self.name, name))[1:]
        if key in self.backend:
            return self.backend[key]
        grp = self.backend[key] = LeanGroup(self.backend, key)
        return grp
