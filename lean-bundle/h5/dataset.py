import h5py
import numpy as np
from .datatypes import KEY_VALUE_DT
from utils.json import JSONObject

class LeanDataset(object):
    def __init__(self, group, name):
        self.group = group
        self.name = name
        self.data = []

    def write(self):
        #empty dataset
        if len(data) == 0:
            self.group.create_dataset(self.name, dtype='f')
            return
        #write data
        if self.name in self.group:
            #extending data (should almost not happen, rarely?)
            dset = self.group[self.name]
            dset.resize((dset.shape[0] + len(self.data),))
            dset[-len(data):] = self.data
        else:
            #creating new dataset (default case)
            self.group.create_dataset(self.name, data=data, maxshape=(None,), dtype=KEY_VALUE_DT)

    def from_json(self, json):
        self.data = []
        for k,v in json.items():
            self.data.append((str(k), JSONObject.dumps(v)))
    
    def to_json(self):
        #TODO: read dataset and convert based on key-values to json
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            return
        self.write()
