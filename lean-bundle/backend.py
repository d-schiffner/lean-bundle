import os

if os.getenv('LEAN_BACKEND', 'lmdb') == 'h5':
    print("Using H5 backend")
    from h5 import *
else:
    print("Using LMDB backend")
    from lm import *
