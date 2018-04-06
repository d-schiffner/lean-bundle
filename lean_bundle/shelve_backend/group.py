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
    
    def _get_container_data(self, name):
        fullpath = path.join(self.name, name)
        dir, key = path.split(fullpath)
        if dir != self.name:
            container = self.backend.find_parent(dir, True)
        else:
            container = self
        return (container, fullpath, key)

    def create_group(self, name):
        container, fullpath, key = self._get_container_data(name)
        if key in container:
            raise Exception("Key {} already exists".format(fullpath))
        container[key] = LeanGroup(self.backend, fullpath)
        return container[key]

    def require_group(self, name):
        container, fullpath, key = self._get_container_data(name)
        if key in container:
            return container[key]
        container[key] = LeanGroup(self.backend, fullpath)
        return container[key]

    def __repr__(self):
        return "Group {} [{}]: {}".format(self.name, len(self.nodes), self._attrs)