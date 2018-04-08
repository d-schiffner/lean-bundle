#Demo script
from lean_bundle.backend import *
from re import compile as re_compile

def main(bundle):
    #don't use cache, we don't reuse the entries
    bundle.use_cache = False
    #search the anwsered path
    inter = bundle['/interaction/adlnet.gov/expapi/verbs/answered'].name
    count = 0
    #bundle.storage.writeback = False
    matcher = re_compile('\/user\/.+\/.+\/.+\/\d+')
    for k in bundle:
        path = str(k)
        #mass parallelise
        if matcher.match(path):
            action = bundle[path].attrs.get('interaction_type', None)
            if action and action.name == inter:
                count += 1
    print(count)
