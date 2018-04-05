import os
from fdict import sfdict

class LeanFile():
    def __init__(self, filename, mode=None):
        if mode == 'w' and os.path.exists(filename):
            os.remove(filename)
        self.storage = sfdict(filename=filename)
        self._setup()

    def __getitem__(self, name):
        tmp = self.storage['root']
        tmp.backend = self
        return tmp[name]
    
    def _setup(self):
        from .group import LeanGroup
        #create root (empty path)
        if not 'root' in self.storage:
            self.storage['root'] = LeanGroup(self, '/')
        self.root = self.storage['root']
        self.root.require_group('/user')
        self.root.require_group('/interaction')
        self.root.require_group('/lo')

    def find_parent(self, path):
        parts = path.split('/')
        assert parts[0] == ''
        parts = parts[1:-1]
        cur = self.root
        traversed = []
        for p in parts:
            if p in cur:
                cur = cur[p]
                traversed.append(p)
            else:
                return None
        return cur

    def sync(self):
        print("PERFORMANCE WARNING")
        self.storage.sync()

    def close(self):
        self.storage.sync()
        print("Dumping")
        for k in self.storage.keys():
            print(k)
        self.storage.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.sync()
        self.close() 
