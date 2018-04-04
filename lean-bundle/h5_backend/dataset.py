import h5py
import numpy as np
from os import getenv
from .datatypes import KEY_VALUE_DT
from utils.json import JSONObject
from utils.writable import Writable


class LeanDataset(Writable):
    STORAGE_METHOD = getenv('LEAN_DATASET_H5_STORAGE', 'dataset').lower()
    def __init__(self, parent, name):
        super().__init__()
        self.parent = parent.h5obj
        self.name = name
        self.data = {}

    def _as_attributes(self):
        group = self.parent.require_group(self.name)
        for k,v in self.data:
            group.attrs[k] = v
        
    def _as_dataset(self):
        #transform data
        tmpdata = [(k,v) for k,v in self.data.items()]
        if len(self.data) == 0:
            self.parent.create_dataset(self.name, dtype='f', shape=(1,))
        elif self.name in self.parent:
            #extending data (should almost not happen, rarely?)
            dset = self.parent[self.name]
            dset.resize((dset.shape[0] + len(self.data),))
            dset[-len(data):] = tmpdata
        else:
            #creating new dataset (default case)
            dset = self.parent.create_dataset(self.name, shape=(len(self.data),), maxshape=(None,), dtype=KEY_VALUE_DT)
            dset[...] = tmpdata

    def write(self):
        #write data
        getattr(self, "_as_" + LeanDataset.STORAGE_METHOD)()
        return self

    def from_json(self, json):
        if not hasattr(json, 'items'):
            return self
        self.data.clear()
        for k,v in json.items():
            self.data[str(k)] = JSONObject.dumps(v)
        return self
    
    def to_json(self):
        #TODO: read dataset and convert based on key-values to json
        pass
