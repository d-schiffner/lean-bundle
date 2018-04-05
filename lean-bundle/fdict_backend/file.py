import os
from fdict import sfdict

class LeanFile(sfdict):
    def __init__(self, filename, mode=None):
        if mode == 'w' and os.path.exists(filename):
            os.remove(filename)
        super().__init__(filename=filename)
        self._setup()

    def __getitem__(self, name):
        #TODO: Register in parent
        obj = super().__getitem__(name)
        obj.backend = self
        return obj

    def _setup(self):
        from .group import LeanGroup
        #create root (empty path)
        if not '' in self:
            self[''] = LeanGroup(self, '')
        root = self['']
        root.require_group('/user')
        root.require_group('/interaction')
        root.require_group('/lo')

    def close(self):
        self.sync()
        print("Dumping")
        for k in self.keys():
            print(k)
        super().close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.sync()
        self.close() 
