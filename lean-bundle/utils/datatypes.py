import h5py
import numpy as np

REF_DT = h5py.special_dtype(ref=h5py.Reference)
KEY_VALUE_DT = np.dtype([('key', h5py.special_dtype(vlen=str)), ('value', h5py.special_dtype(vlen=str))])
#special type for actor object types
__ACTOR_TYPE_MAP__ = {'agent' : 0, 'group': 1}
USER_TYPE_DT = h5py.special_dtype(enum=('i', __ACTOR_TYPE_MAP__))
