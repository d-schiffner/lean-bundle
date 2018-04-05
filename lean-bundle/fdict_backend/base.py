from os import path
from utils.writable import Writable

class LeanAttribs():
    def __init__(self, parent):
        self.parent = parent
    
    def create(self, key, value):
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
        self.data = {}
        self._backend = backend
        #must be here

    def valid(self):
        return self._backend != None

    @property
    def backend(self):
        return self._backend
    
    @backend.setter
    def backend(self, backend):
        self._backend = backend
        #update sub items
        for k,v in self.data.items():
            if isinstance(v, LeanBase):
                v.backend = backend

    @property
    def attrs(self):
        return LeanAttribs(self)

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def __contains__(self, key):
        return path.join(self.name, key) in self.backend

    def __getitem__(self, key):
        #use fast access to sfdict by path encoding
        pathname = path.join(self.name, key)
        #print("Fast lane", pathname)
        return self.backend[pathname]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['_backend']
        return d

    def __setstate__(self, obj):
        self.__dict__ = obj

    def sync(self):
        pass

    def __repr__(self):
        return "Obj {} ({})".format(self.name, hex(id(self)))
