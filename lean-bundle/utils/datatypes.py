import h5py
import numpy as np

REF_DT = h5py.special_dtype(ref=h5py.Reference)
KEY_VALUE_DT = np.dtype([('key', h5py.special_dtype(vlen=str)), ('value', h5py.special_dtype(vlen=str))])
#special type for actor object types
ACTOR_TYPE_MAP = {'agent' : 0, 'group': 1}
INTERACTIVE_LO_TYPE_MAP = {'choice': 0}

USER_TYPE_DT = h5py.special_dtype(enum=('i', ACTOR_TYPE_MAP))
INTERACTIVE_LO_DT = h5py.special_dtype(enum=('i', INTERACTIVE_LO_TYPE_MAP))
