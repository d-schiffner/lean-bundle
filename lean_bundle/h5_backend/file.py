import h5py

class LeanFile(h5py.File):
    def __init__(self, filename, mode=None):
        super().__init__(filename, mode)
        #default
        self.require_group('/user')
        self.require_group('/lo')
        self.require_group('/interaction')

    def __getitem__(self, name):
        h5obj = super().__getitem__(name)
        if isinstance(h5obj, h5py.Group):
            from .group import LeanGroup
            return LeanGroup(h5obj)
        return h5obj
    
    def sync(self):
        pass