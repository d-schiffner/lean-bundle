import numpy as np
import h5py
from .datatypes import *
from .json import JSONObject
from .error import MissingConverterError

   
class LeanGroup(object):
    def __init__(self, group):
        self.group = group

    #JSON to HDF5
    def from_json(self, json, ignore=[]):
        if not hasattr(json, 'items'):
            return
        for k,v in json.items():
            tv = type(v)
            if k in ignore:
                continue
            if tv is str:
                self.group.attrs.create(k,v, dtype=h5py.special_dtype(vlen=str))
            elif tv is bool:
                self.group.attrs[k] = v
            elif isinstance(v, JSONObject):
                with LeanDataset(self.group, k) as lgd:
                    lgd.from_json(v)
            else:
                raise MissingConverterError("Unknown type: {}".format(type(v)))
    #HDF5 to json
    def to_json(self, json):
        #read all attrs and datasets and convert them to json
        pass
