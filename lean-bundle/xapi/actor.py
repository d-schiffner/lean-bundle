from utils.json import JSONObject
from utils.datatypes import USER_TYPE_DT, ACTOR_TYPE_MAP


def create_user(authority_grp, xapi):
    #creates a bundle group
    actor = xapi.statement.actor
    name = actor.name if actor.name else 'anon'
    #check for group
    if name in authority_grp:
        return authority_grp[name]
    #doesn't exist -> create
    user_grp = authority_grp.create_group(name)
    #set the group's attributes
    user_grp.attrs.create('type', ACTOR_TYPE_MAP[actor.objectType.lower()], dtype=USER_TYPE_DT)
    return user_grp