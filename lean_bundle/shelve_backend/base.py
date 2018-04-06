from os import path
from utils.writable import Writable

class LeanAttribs():
    def __init__(self, parent):
        self.parent = parent
    
    def keys(self):
        return self.parent._attrs.keys()
        
    def create(self, key, value):
        self.parent._attrs[key] = value

    def modify(self, key, value):
        self.parent._attrs[key] = value
    
    def __contains__(self, key):
        return key in self.parent._attrs

    def __getitem__(self, key):
        return self.parent._attrs[key]

    def __setitem__(self, key, value):
        self.parent._attrs[key] = value


class LeanBase(Writable):
    def __init__(self, backend, name):
        super().__init__()
        self.name = name
        #print("Lean Base:",name)
        self._attrs = {}
        #store direct children here for fast lookup
        self.nodes = set()
        self._backend = backend

    def valid(self):
        return self._backend != None

    @property
    def backend(self):
        return self._backend
    
    @backend.setter
    def backend(self, backend):
        self._backend = backend

    @property
    def ref(self):
        return self
    @property
    def attrs(self):
        return LeanAttribs(self)

    def items(self):
        for k in self.keys():
            yield k, self[k]

    def keys(self):
        return sorted(self.nodes)

    def values(self):
        for k in self.keys():
            yield self[k]

    def __contains__(self, name):
        fullpath = path.join(self.name, name)
        return fullpath in self.backend.storage

    def __getitem__(self, name):
        fullpath = path.join(self.name, name)
        item = self._backend.storage[fullpath]
        #may be loaded from file -> set backend
        item._backend = self._backend
        return item

    def __setitem__(self, name, value):
        fullpath = path.join(self.name, name)
        directory, key = path.split(fullpath)
        if directory != self.name:
            container = self._backend.find_parent(directory)
        else:
            container = self
        #store lookup
        container.nodes.add(key)
        self._backend.storage[fullpath] = value

    def __getstate__(self):
        d = self.__dict__.copy()
        if '_backend' in d:
            del d['_backend']
        return d

    def __setstate__(self, obj):
        self.__dict__ = obj

    def sync(self):
        #self.backend.sync()
        pass

    def __repr__(self):
        return "Obj {} ({})".format(self.name, hex(id(self)))
