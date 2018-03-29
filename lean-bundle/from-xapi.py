import h5py
import numpy as np
import sys
import json
import time
from argparse import ArgumentParser
from utils.json import JSONObject
from utils.group import LeanGroup, LeanDataset
from utils.datatypes import *
from xapi import actor, authority, date


def create_choice_lo(lo, definition):
    #create a choice lo structure
    lo.attrs['type'] = 'choice'
    choices = lo.create_group('choices')
    correctResponses = definition.correctResponsesPattern if 'correctResponsesPattern' in definition else []
    for obj in definition.choices:
        c = choices.create_group(obj.id)
        for k,v in obj.items():
            if k == 'id':
                continue
            #create a dataset from json
            LeanDataset(c, k).from_json(v)
        c.attrs.create('correct', obj.id in correctResponses)
    #write out remaining data
    LeanGroup(lo).from_json(definition, ['choices', 'type', 'correctResponsesPattern'])

url2LO = {}
def find_matching(los, object):
    global url2LO
    #TODO: this needs to be faster!!!
    if object.id in url2LO:
        return url2LO[object.id]
    return None

def create_lo(bundle, statement):
    global url2LO
    object = statement.object
    los = bundle.require_group('/lo')
    #find existing ones
    new_lo = find_matching(los, object)
    if new_lo:
        return new_lo
    nid = len(los.keys())
    #print("Creating a new lo")
    new_lo = los.create_group(str(nid))
    new_lo.attrs['url'] = object.id
    url2LO[object.id] = new_lo
    #TODO: identify authority of lo?
    new_lo.attrs['auth'] = 'anon'
    if 'definition' in object:
        definition = object.definition
        #check for interactionTypes
        if 'interactionType' in definition:
            if definition.interactionType == 'choice':
                create_choice_lo(new_lo, definition)
            else:
                raise NotImplementedError("Unknown interaction type: {}".format(definition.interactionType))
        else:
            LeanGroup(new_lo).from_json(definition)
    return new_lo

def update_context_of_lo(lo, statement):
    #check for context
    if 'context' in statement and statement.context:
        #TODO: Create context
        lo.attrs.create('hasContext', True)

def create_interaction(fibers, bundle, statement):
    #create an interaction if not present, link to it
    verb = statement.verb
    if verb.id.startswith('http://adlnet.gov/expapi/verbs'):
        auth = "adl"
        id = verb.id[31:]
    else:
        auth = verb.id[7:]
        auth = auth[:auth.find('/')]
        id = verb.id[verb.id.rfind('/'):]
    #print("Interaction is {}/{}".format(auth,id))
    #TODO: Add display/description to interaction
    interaction = bundle.require_group('/interaction/{}/{}'.format(auth, id))
    #TODO: Check if we want to automatically add counts for each interaction
    #create data
    data = [interaction.ref]
    #create a learning object based on the object (if it does not refer to a user or another statement)
    object = statement.object
    #print("Type: {}".format(object.objectType.lower()))
    if object.objectType.lower() == 'activity':
        #object references an lo
        #create it
        learning_object = create_lo(bundle, statement)
        update_context_of_lo(learning_object, statement)
        data.append(learning_object.ref)
        #print("Created activity entry")
    else:
        raise NotImplementedError(object.objectType, "not implemented yet")
    #store refs in fiber
    dset = fibers.create_dataset('interaction', (len(data),), dtype=REF_DT)
    dset[...] = data


def add_statement(bundle, xapi):
    #read user
    statement = xapi.statement
    #print("Found statement: {} {} {}".format(statement.actor.name, statement.verb.id, statement.object.id))
    #create authority
    auth_grp = bundle.require_group('/user/{}'.format(authority.get(statement)))
    #create user group if not existing
    user_grp = actor.create_user(auth_grp, xapi)
    #TODO: how to identify configuration?
    config_grp = user_grp.require_group('general')
    #create timestamp entry
    time = str(date.timestamp(xapi, 'timestamp'))
    if time in config_grp:
        #this timestamp is already in here!
        #TODO: Sanity check!
        return
    fibers = config_grp.create_group(time)
    #create fibers
    create_interaction(fibers, bundle, statement)
    fibers.attrs.create('stored', date.timestamp(xapi,'stored'))
    if 'result' in statement:
        #TODO: Better parsing?
        LeanGroup(fibers).from_json(statement.result)
    #print("Statement added")

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Bundle xAPI Parser")
    parser.add_argument('--out', required=True)
    parser.add_argument('--replace', '-r', help="Replace the file with the new content", action='store_true')
    parser.add_argument('--bench', action='store_true', help="Benchmark the app")
    parser.add_argument('--skip', default=0, help="Skip the first x entries", type=int)
    parser.add_argument('file', help="The file to read the xAPI Statements from")

    args = parser.parse_args()
    print("Converting xAPI from JSON to LeAn Bundle")
    print("Creating file {}".format(args.out))
    if(args.replace):
        print("Replacing content in bundle")
        f = h5py.File(args.out, 'w')
    else:
        print("Appending to existing bundle")
        f = h5py.File(args.out)
    
    if(args.bench):
        start = time.perf_counter()
    with open(args.file, 'r') as data_file:
        count = 0
        for line in data_file:
            count += 1
            if count < args.skip:
                continue
            print("Statement {}".format(count), end="\r")
            xapi = json.loads(line, object_hook=JSONObject)
            if 'statement' in xapi:
                try:
                    add_statement(f, xapi)
                except Exception as e:
                    import traceback
                    #print empty line to preserve counter
                    print('')
                    print(count)
                    print(e)
                    traceback.print_exc()
                    print(xapi)
                    #sys.exit(1)
            else:
                print("No statement in line {}".format(count))
        print('')
    f.close()
    if(args.bench):
        end = time.perf_counter()
        print("Needed {} ms".format((end-start)*1000))
    print("Program finished")