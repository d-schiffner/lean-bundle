import numpy as np
import h5py
from .datatypes import *
from .json import JSONObject
from .error import MissingConverterError


class LeanDataset(object):
    def __init__(self, group, name):
        self.group = group
        self.name = name

    def from_json(self, json):
        data = []
        for k,v in json.items():
            #TODO: Compare behavior if subgroups are generated instead
            data.append((str(k), JSONObject.dumps(v)))
        if self.name in self.group:
            #extending data (should almost not happen, rarely?)
            dset = self.group[self.name]
            dset.resize((dset.shape[0] + len(data),))
            dset[-len(data):] = data
        else:
            #creating new dataset (default case)
            dset = self.group.create_dataset(self.name, (len(data),), maxshape=(None,), dtype=KEY_VALUE_DT)
            dset[...] = data
    
    def to_json(self):
        #TODO: read dataset and convert based on key-values to json
        pass
    
class LeanGroup(object):
    def __init__(self, group):
        self.group = group

    #JSON to HDF5
    def from_json(self, json, ignore=[]):
        for k,v in json.items():
            tv = type(v)
            if k in ignore:
                continue
            if tv is str:
                self.group.attrs.create(k,v, dtype=h5py.special_dtype(vlen=str))
            elif tv is bool:
                self.group.attrs[k] = v
            elif isinstance(v, JSONObject):
                lgd = LeanDataset(self.group, k)
                lgd.from_json(v)
            else:
                raise MissingConverterError("Unknown type: {}".format(type(v)))
    #HDF5 to json
    def to_json(self, json):
        #read all attrs and datasets and convert them to json
        pass