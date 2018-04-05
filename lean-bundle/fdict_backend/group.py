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
        fullpath, key = path.split(path.join(self.name, name))
        print("Searching parent", fullpath)
        container = self.backend.find_parent(fullpath)
        print("Parent is", container)
        if key in container:
            raise Exception("Key {} already exists".format(key))
        container[key] = LeanGroup(self.backend, key)
        return container[key]

    def require_group(self, name):
        fullpath, key = path.split(path.join(self.name, name))
        print("Searching parent", fullpath)
        container = self.backend.find_parent(fullpath)
        print("Found", container)
        if key in container:
            return container[key]
        container[key] = LeanGroup(self.backend, key)
        return container[key]
