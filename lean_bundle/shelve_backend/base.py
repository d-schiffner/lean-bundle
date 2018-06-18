from os import path
from ..utils.writable import Writable

class LeanAttribs():
    def __init__(self, parent):
        self.parent = parent
    
    def keys(self):
        return self.parent._attrs.keys()
        
    def create(self, key, value):
        self.parent._attrs[key] = value

    def modify(self, key, value):
        self.parent._attrs[key] = value
    
    def get(self, key, default):
        return self.parent._attrs.get(key, default)
        
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
        self.backend = backend

    def valid(self):
        return self.backend != None

    @property
    def ref(self):
        return LeanRef(self.backend, self.name)

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
        item = self.backend.storage[fullpath]
        #may be loaded from file -> set backend
        item.backend = self.backend
        return item

    def __setitem__(self, name, value):
        fullpath = path.join(self.name, name)
        directory, key = path.split(fullpath)
        if directory != self.name:
            container = self.backend.find_parent(directory)
        else:
            container = self
        #store lookup
        container.nodes.add(key)
        self.backend.storage[fullpath] = value
        #restore parent
        #self.backend.storage[container.name] = container

    def __getstate__(self):
        d = self.__dict__.copy()
        if 'backend' in d:
            del d['backend']
        return d

    def sync(self):
        #self.backend.sync()
        pass

    def __repr__(self):
        return "Obj {} ({})".format(self.name, hex(id(self)))

class LeanRef(Writable):
    def __init__(self, backend, name):
        self.backend = backend
        self.name = name

    @property
    def ref(self):
        print("WARNING: You want to use ref to ref??")
        return self

    @property
    def target(self):
        if not self._target:
            self._target = self.backend.storage[self.name]
        return self._target

    @property
    def attrs(self):
        return self.target.attrs

    def __getitem__(self, name):
        return self.target[name]
    
    def __setitem__(self, name, value):
        self.target[name] = value

    def __contains__(self, key):
        return key in self.target
    
    def items(self):
        return self.target.items()

    def keys(self):
        return self.target.keys()

    def values(self):
        return self.target.values()

    def sync(self):
        self.target.sync()

    def __getstate__(self):
        d = self.__dict__.copy()
        if '_target' in d:
            del d['_target']
        if 'backend' in d:
            del d['backend']
        return d

    def __setstate__(self, obj):
        self.__dict__ = obj

    def __repr__(self):
        return "Ref {}".format(self.name)

       