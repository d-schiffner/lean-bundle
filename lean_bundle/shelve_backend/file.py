import os
import shelve

class LeanFile():
    def __init__(self, filename, mode=None):
        self.mode = mode
        if mode and 'w' in mode and os.path.exists(filename):
            os.remove(filename)
        self.filename = filename
        self.storage = shelve.open(self.filename, writeback=True)
        self._setup()

    def __getitem__(self, name):
        tmp = self.storage['root']
        tmp.backend = self
        if name == '/':
            return tmp
        return tmp[name]
    
    def _setup(self):
        from .group import LeanGroup
        #create root (empty path)
        if not 'root' in self.storage:
            self.storage['root'] = LeanGroup(self, '/')
        self.root = self.storage['root']
        #store backend in case it has been retreived
        self.root.backend = self
        self.root.require_group('/user')
        self.root.require_group('/interaction')
        self.root.require_group('/lo')
        self.root.require_group('/scripts')

    def find_parent(self, path, create=False):
        from .group import LeanGroup
        if path == '/':
            return self.root
        parts = path.split('/')
        assert parts[0] == ''
        parts = parts[1:]
        if parts[0] == '':
            return self.root
        cur = self.root
        traversed = []
        for p in parts:
            if not isinstance(cur, LeanGroup):
                return None
            if p in cur.nodes:
                cur = cur[p]
                cur._backend = self
            elif create:
                #create
                cur = cur.create_group(p)
            else:
                return None
            traversed.append(p)
        return cur

    def sync(self):
        print("PERFORMANCE WARNING")
        self.storage.sync()

    def close(self):
        self.storage.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close() 
