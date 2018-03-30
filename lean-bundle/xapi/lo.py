import numpy as np
import hashlib
from xapi import authority, actor
from utils.group import LeanDataset, LeanGroup
from utils.datatypes import INTERACTIVE_LO_DT, INTERACTIVE_LO_TYPE_MAP
from utils.error import MissingConverterError
__URL2LO = {}
__CONTEXT = {}

def _create_choice_lo(lo, definition):
    global __CHOICE_TYPE
    #create a choice lo structure
    lo.attrs.create('type', INTERACTIVE_LO_TYPE_MAP['choice'], dtype=INTERACTIVE_LO_DT)
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

def _find_matching(los, object):
    global __URL2LO
    return __URL2LO[object.id] if object.id in __URL2LO else None


def update_context(lo, statement):
    global __CONTEXT
    #check for context
    if 'context' in statement and statement.context:
        #TODO: define good hash
        sha = hashlib.sha1(str(",".join(sorted([k for k,v in statement.context.items()]))).encode()).hexdigest()
        if 'context' in lo:
            if lo['context'].attrs['hash'] != sha:
                #TODO: Define what to do
                pass
        else:
            ctx_grp = lo.create_group('context')
            ctx = statement.context
            if 'instructor' in ctx:
                auth_grp = authority.get(lo, statement)
                user_grp = actor.create_user(auth_grp, ctx.instructor)
                ctx_grp.attrs['instructor'] = user_grp.ref
            if 'statement' in ctx:
                raise MissingConverterError('StatementRefs not implemented')
            LeanGroup(ctx_grp).from_json(ctx, ignore=['instructor', 'statement'])
            ctx_grp.attrs['hash'] = sha


def _create(bundle, statement):
    #Default creation method
    global __URL2LO
    object = statement.object
    los = bundle.require_group('/lo')
    #find existing ones
    new_lo = _find_matching(los, object)
    if new_lo:
        return new_lo
    nid = len(los.keys())
    #print("Creating a new lo")
    new_lo = los.create_group(str(nid))
    new_lo.attrs['url'] = object.id
    __URL2LO[object.id] = new_lo
    #TODO: identify authority of lo?
    new_lo.attrs['auth'] = 'anon'
    if 'definition' in object:
        definition = object.definition
        #check for interactionTypes
        if 'interactionType' in definition:
            if definition.interactionType == 'choice':
                _create_choice_lo(new_lo, definition)
            else:
                raise MissingConverterError("Unknown interaction type: {}".format(definition.interactionType))
        else:
            LeanGroup(new_lo).from_json(definition)
    return new_lo

def create(bundle, statement):
    lo = _create(bundle, statement)
    update_context(lo, statement)
    return lo