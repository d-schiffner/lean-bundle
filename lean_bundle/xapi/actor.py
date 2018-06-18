import logging
from ..utils.json import JSONObject
from ..utils.datatypes import ACTOR_TYPE_MAP

__log = logging.getLogger()

def create_user(authority_grp, actor):
    #creates a bundle group
    name = actor.name if actor.name else 'anon'
    #check for group
    if name in authority_grp:
        return authority_grp[name]
    #doesn't exist -> create
    user_grp = authority_grp.create_group(name)
    #set the group's attributes
    user_grp.attrs.create('type', ACTOR_TYPE_MAP[actor.objectType.lower()])
    if 'account' in actor:
        if 'mbox' in actor.account:
            user_grp.attrs['mbox'] = actor.account.mbox
        if 'homePage' in actor.account:
            user_grp.attrs['homepage'] = actor.account.homePage
        if "name" in actor.account:
            user_grp.attrs["name"] = actor.account.name
    else:
        __log.warn("Unknown params %s", actor)
    #TODO: set other keys
    return user_grp
