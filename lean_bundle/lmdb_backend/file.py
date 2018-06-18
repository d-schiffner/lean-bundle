import lmdb
import os

class LeanFile(object):
    def __init__(self, filename, mode=None):
        if mode == 'w':
            os.remove(filename)
        self.env = lmdb.open(filename, subdir=False, map_size=1024**4)
        with self.env.begin(write=True) as txn:
            if not txn.get(b'/user'):
                txn.put(b'/user', b'')
            if not txn.get(b'/lo'):
                txn.put(b'/lo', b'')
            if not txn.get(b'/interaction'):
                txn.put(b'/interaction', LeanGroup())


    def __getitem__(self, name):
        pass

    def close():
        self.env.close()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()