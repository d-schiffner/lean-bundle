from lean_bundle.backend import *
from re import compile as re_compile

def main(bundle):
    #don't use cache, we don't reuse the entries
    bundle.use_cache = False
    count = {}
    #bundle.storage.writeback = False
    matcher = re_compile('\/user\/.+\/.+\/.+\/\d+')
    for k in bundle:
        path = str(k)
        #mass parallelise
        if matcher.match(path):
            action = bundle[path].attrs.get('interaction_target', None)
            if action:
                #compute user
                username = path.split('/')[3]
                tmp = count.get(username, set())
                tmp.add(action.name)
                count[username] = tmp
    for k,v in count.items():
        print(k, len(v))
