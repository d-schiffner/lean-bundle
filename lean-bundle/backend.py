import os

_requested_backend = os.getenv('LEAN_BACKEND', 'shelve')
if _requested_backend == 'h5':
    print("Using H5 backend")
    from h5_backend import *
elif _requested_backend == 'lmdb':
    print("Using LMDB backend")
    from lmdb_backend import *
elif _requested_backend == 'shelve':
    print("Using shelve backend")
    from fdict_backend import *
else:
    raise ImportError('Unknown backend')
