from utils.datatypes import USER_TYPE_DT, ACTOR_TYPE_MAP

def get(bundle, statement):
    if not 'authority' in statement or not 'name' in statement.authority:
        return bundle.require_group('/user/anon')
    auth = statement.authority
    if auth.name in bundle['/user']:
        return bundle['/user/'+auth.name]
    auth_grp = bundle.create_group('/user/{}'.format(auth.name))
    if 'objectType' in auth:
        auth_grp.attrs.create('type', ACTOR_TYPE_MAP[auth.objectType.lower()], dtype=USER_TYPE_DT)
    if 'mbox' in auth:
        auth_grp.attrs['mbox'] = auth.mbox
    #TODO: check for others
    return auth_grp
