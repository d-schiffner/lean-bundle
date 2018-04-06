from utils.datatypes import ACTOR_TYPE_MAP

def name(statement):
    return  statement.authority.name if not 'authority' in statement or not 'name' in statement.authority else 'anon'
    
def get(bundle, statement):
    user_grp = bundle['/user']
    if not 'authority' in statement or not 'name' in statement.authority:
        return user_grp.require_group('anon')
    auth = statement.authority
    if auth.name in user_grp:
        return user_grp[auth.name]
    auth_grp = user_grp.create_group(auth.name)
    if 'objectType' in auth:
        auth_grp.attrs.create('type', ACTOR_TYPE_MAP[auth.objectType.lower()])
    if 'mbox' in auth:
        auth_grp.attrs['mbox'] = auth.mbox
    #TODO: check for others
    return auth_grp
