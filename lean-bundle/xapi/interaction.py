import h5py
import numpy as np
from xapi import lo
from utils.group import LeanDataset, LeanGroup
from utils.datatypes import REF_DT
from utils.error import MissingConverterError

class InteractionCreator():
    def __init__(self, bundle, statement):
        self.statement = statement
        self.bundle = bundle
        self.id = None
        self.extract_id()

    @property
    def path(self):
        return '/interaction/{}'.format(self.id)

    def extract_id(self):
        verb = self.statement.verb
        #interpret uri as path in interaction
        self.id = verb.id[7:]
        #fallback, if https is used
        if self.id[0] == '/':
            self.id = self.id[1:]

    def create(self):
        path = self.path
        if path in self.bundle:
            self.group = self.bundle[path]
            self.check_definition()
        else:
            self.group = self.bundle.create_group(path)
            self.write_definition()
        self.write_context()

    def write_definition(self):
        verb = self.statement.verb
        if 'display' in verb:
            LeanDataset(self.group, 'display').from_json(verb.display)

    def check_definition(self):
        if 'display' in self.statement.verb and not 'display' in self.group:
            print("WARN: Definition was missing for {}".format(self.group.name))
            self.write_definition()
    
    def write_context(self):
        #TODO: Specify and extract user behavior specific context data
        pass


def create(fibers, bundle, statement):
    #print("Interaction is {}/{}".format(auth,id))
    inter = InteractionCreator(bundle, statement)
    inter.create()
    #TODO: Check if we want to automatically trace uses!?
    #create data for fiber
    data = [inter.group.ref]
    #create a learning object based on the object (if it does not refer to a user or another statement)
    object = statement.object
    #print("Type: {}".format(object.objectType.lower()))
    if object.objectType.lower() == 'activity':
        #object references an lo
        #create it
        learning_object = lo.create(bundle, statement)
        data.append(learning_object.ref)
        #print("Created activity entry")
    else:
        raise MissingConverterError(object.objectType, "not implemented yet")
    #store refs in fiber
    #NOTE: Direct creation of dataset
    fibers.create_dataset('interaction', data=data, dtype=REF_DT)
    #NOTE: Indirect creation of dataset -> equivalent in size to direct creation
    #dset = fibers.create_dataset('interaction', (len(data),), dtype=REF_DT)
    #dset[...] = data
    #NOTE: Empty dataset
    #dset = fibers.create_dataset("interaction", dtype="f")
    #dset.attrs['type'] = data[0]
    #dset.attrs['target'] = data[1]
    #NOTE: storage as group of attributes -> worst!
    #actions = fibers.create_group('interaction')
    #actions.attrs['type'] = data[0]
    #actions.attrs['target'] = data[1]
    #NOTE: storage as direct attributes
    #fibers.attrs['interaction_type'] = data[0]
    #fibers.attrs['interaction_target'] = data[1]
    #NOTE: compact dataspace dataset
    #space_id = h5py.h5s.create_simple((2,))
    #dcpl = h5py.h5p.create(h5py.h5p.DATASET_CREATE)
    #dcpl.set_layout(h5py.h5d.COMPACT)
    #dset = h5py.h5d.create(bundle.id, (fibers.name + "/interaction").encode(), h5py.h5t.STD_REF_OBJ, space_id, dcpl)
    #dset.write(h5py.h5s.ALL, h5py.h5s.ALL, np.asarray(data))
    #del dcpl
    #del space_id
    #del dset
