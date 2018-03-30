import numpy as np
from utils.group import LeanDataset, LeanGroup
from utils.datatypes import INTERACTIVE_LO_DT, INTERACTIVE_LO_TYPE_MAP


__URL2LO = {}
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
    #check for context
    if 'context' in statement and statement.context and not 'hasContext' in lo.attrs:
        #TODO: Create context
        lo.attrs.create('hasContext', True)


def _create(bundle, statement):
    #Default creation method
    global __URL2LO
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
    __URL2LO[object.id] = new_lo
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

def create(bundle, statement):
    lo = _create(bundle, statement)
    update_context(lo, statement)
    return lo