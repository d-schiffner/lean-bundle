import hashlib
from . import authority, actor
from ..utils.datatypes import INTERACTIVE_LO_TYPE_MAP
from ..utils.error import MissingConverterError
from ..backend import *

__URL2LO = {}


def _create_choice_lo(lo, definition):
    #create a choice lo structure
    lo.attrs.create('type', INTERACTIVE_LO_TYPE_MAP['choice'])
    choices = lo.create_group('choices')
    correctResponses = definition.correctResponsesPattern if 'correctResponsesPattern' in definition else []
    for obj in definition.choices:
        c = choices.create_group(obj.id)
        for k,v in obj.items():
            if k == 'id':
                continue
            #create a dataset from json
            with LeanDataset(c, k) as lgd:
                lgd.from_json(v)
        c.attrs.create('correct', obj.id in correctResponses)
    #write out remaining data
    lo.from_json(definition, ['choices', 'type', 'correctResponsesPattern']).sync()

def _find_matching(los, object):
    global __URL2LO
    return __URL2LO[object.id] if object.id in __URL2LO else None


def _create(bundle, statement):
    #Default creation method
    global __URL2LO
    object = statement.object
    #/lo is assured to exist
    los = bundle['/lo']
    #find existing ones
    new_lo = _find_matching(los, object)
    if new_lo:
        return new_lo
    nid = len(los.keys())
    #print("Creating a new lo")
    new_lo = los.create_group('lo'+str(nid))
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
            new_lo.from_json(definition).sync()
    return new_lo

def create(bundle, statement):
    lo = _create(bundle, statement)
    #update_context(lo, statement)
    return lo
