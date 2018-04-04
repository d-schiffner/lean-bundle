from os import path
from lmdb import 


class LeanBase():
    def __init__(self, name, backend):
        self.name = path.abspath(name)
        self.backend = backend
        self.attrs = dict()
    
    def __getitem__(self, x):
        if not path.isabs(x):
            x = path.abspath(path.join(self.name, x))
        return self.backend[x]
    
    def __getstate__(self):
        d = dict()
        d['name'] = self.name
        d['attrs'] = self.attrs.copy()
        return d
