from lean_bundle.backend import *

def main(bundle):
    bundle.use_cache = False
    auth = bundle['/user']
    count = 0
    for k in auth.keys():
        users = auth[k]
        count += len(users.keys())
    print(count)