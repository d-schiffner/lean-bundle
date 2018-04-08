import numpy as np
import h5py
from .datatypes import *
from .dataset import LeanDataset
from utils.json import JSONObject
from utils.error import MissingConverterError
from utils.writable import Writable
   
class LeanGroup(Writable):
    def __init__(self, h5obj):
        super().__init__()
        self.h5obj = h5obj
        self.data = {}

    @property
    def attrs(self):
        return self.h5obj.attrs

    @property
    def ref(self):
        return self.h5obj.ref

    def keys(self):
        return self.h5obj.keys()

    def create_group(self, name):
        grp = self.h5obj.create_group(name)
        return LeanGroup(grp)

    def require_group(self, name):
        grp = self.h5obj.require_group(name)
        return LeanGroup(grp)

    def sync(self):
        for k,v in self.data.items():
            tv = type(v)
            if tv is [str, bool]:
                self.h5obj.attrs[k] = v
            elif isinstance(v, JSONObject):
                with LeanDataset(self, k) as lgd:
                    lgd.from_json(v)

    #JSON to HDF5
    def from_json(self, json, ignore=[]):
        if not hasattr(json, 'items'):
            return self
        for k,v in json.items():
            if k in ignore:
                continue
            self.data[k] = v
        return self

    #HDF5 to json
    def to_json(self, json):
        #read all attrs and datasets and convert them to json
        pass

    def __contains__(self, val):
        return val in self.h5obj

    def __getitem__(self, name):
        elm = self.h5obj[name]
        if isinstance(elm, h5py.Group):
            return LeanGroup(elm)
        return elm
