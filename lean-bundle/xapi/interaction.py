import h5py
import numpy as np
from xapi import lo
from os import getenv
from utils.error import MissingConverterError
from backend import *

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
            LeanDataset(self.group, 'display').from_json(verb.display).write()

    def check_definition(self):
        if 'display' in self.statement.verb and not 'display' in self.group:
            print("WARN: Definition was missing for {}".format(self.group.name))
            self.write_definition()
    
    def write_context(self):
        #TODO: Specify and extract user behavior specific context data
        pass


def create(fibers, statement):
    global ONCE
    #print("Interaction is {}/{}".format(auth,id))
    inter = InteractionCreator(fibers, statement)
    inter.create()
    #TODO: Check if we want to automatically trace uses!?
    #create data for fiber
    data = [inter.group]
    #create a learning object based on the object (if it does not refer to a user or another statement)
    object = statement.object
    #print("Type: {}".format(object.objectType.lower()))
    if object.objectType.lower() == 'activity':
        #object references an lo
        #create it
        learning_object = lo.create(fibers, statement)
        data.append(learning_object)
        #print("Created activity entry")
    else:
        raise MissingConverterError(object.objectType, "not implemented yet")
    #store refs in fiber
    interaction_storage(fibers, data)
