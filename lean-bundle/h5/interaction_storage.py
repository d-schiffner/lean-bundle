#test for interaction storage
import h5py
from .datatypes import REF_DT

def interaction_storage(fibers, data):
    storage_type = getenv('LEAN_INTERACTION_H5_STORAGE', 'ATTRIB').lower()
    if storage_type == 'dset':
        #NOTE: Direct creation of dataset
        fibers.create_dataset('interaction', data=data, dtype=REF_DT)
    elif storage_type == 'dset_indirect':
        #NOTE: Indirect creation of dataset -> equivalent in size to direct creation
        dset = fibers.create_dataset('interaction', (len(data),), dtype=REF_DT)
        dset[...] = data
    elif storage_type == 'empty_dset':
        #NOTE: Empty dataset -> slightly better than dataset
        dset = fibers.create_dataset("interaction", dtype="f")
        dset.attrs['type'] = data[0]
        dset.attrs['target'] = data[1]
    elif storage_type == 'group':
        #NOTE: storage as group of attributes -> worst!
        actions = fibers.create_group('interaction')
        actions.attrs['type'] = data[0]
        actions.attrs['target'] = data[1]
    elif storage_type == 'attrib':
        #NOTE: storage as direct attributes -> best
        fibers.attrs['interaction_type'] = data[0]
        fibers.attrs['interaction_target'] = data[1]
    elif storage_type == 'compact_dset':
        #NOTE: compact dataspace dataset -> worse than default dset
        space_id = h5py.h5s.create_simple((2,))
        dcpl = h5py.h5p.create(h5py.h5p.DATASET_CREATE)
        dcpl.set_layout(h5py.h5d.COMPACT)
        dset = h5py.h5d.create(bundle.id, (fibers.name + "/interaction").encode(), h5py.h5t.STD_REF_OBJ, space_id, dcpl)
        dset.write(h5py.h5s.ALL, h5py.h5s.ALL, np.asarray(data))
        del dcpl
        del space_id
        del dset

# Results on interaction storage
# Vigor first 10k       100k       627k 
# DSET:       18.210kb  179.254kb  x
# Empty DSET: 18.054kb  177.700kb  x
# Comp. DSET: 18.213kb  179.292kb  x
# Group:      23.754kb  234.724kb  x
# Attribs:    13.735kb  132.930kb  799.123kb
# Json:        9.106kb   92.330kb  x
