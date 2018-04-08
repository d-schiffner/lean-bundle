import os
import shelve
from pickle import HIGHEST_PROTOCOL

class LeanFile():
    def __init__(self, filename, mode='c'):
        __pickle_protocol = int(os.getenv('LEAN_PICKLE_PROTOCOL', HIGHEST_PROTOCOL))
        self.mode = mode
        if mode and 'w' == mode:
            self.mode = 'n'
        self.filename = filename
        self.storage = shelve.open(self.filename, flag=self.mode, writeback=True, protocol=__pickle_protocol)
        self._setup()

    @property
    def use_cache(self):
        return self.storage.writeback
    
    @use_cache.setter
    def use_cache(self, value):
        self.storage.writeback = value

    def __getitem__(self, name):
        tmp = self.storage[name]
        tmp.backend = self
        return tmp

    def _setup(self):
        from .group import LeanGroup
        #create root (empty path)
        if not '/' in self.storage:
            self.storage['/'] = LeanGroup(self, '/')
        self.root = self.storage['/']
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
                cur.backend = self
            elif create:
                #create
                cur = cur.create_group(p)
            else:
                return None
            traversed.append(p)
        return cur

    def __iter__(self):
        return self.storage.__iter__()

    def __len__(self):
        return self.storage.__len__()
    
    def __contains__(self, key):
        return self.storage.__contains__(key)

    def sync(self):
        print("PERFORMANCE WARNING")
        #self.storage.sync()

    def close(self):
        #in case we use the cache but we can only read
        if self.mode == 'r':
            #fast bail
            self.storage.dict.close()
            self.storage.dict = None
        self.storage.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close() 
