import h5py

class LeanFile(h5py.File):
    def __init__(self, filename, mode=None):
        super().__init__(filename, mode)
        #default
        self.require_group('/user')
        self.require_group('/lo')
        self.require_group('/interaction')
