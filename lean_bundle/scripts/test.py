from lean_bundle.backend import *

def traverse(group):
    groups = 0
    ds = 0
    attrs = 0
    if isinstance(group, LeanGroup):
        groups = 1
    elif isinstance(group, LeanDataset):
        ds = 1
    else:
        return 0,0,0
    #here only if lean stuff
    attrs = len(group.attrs.keys())
    for k,v in group.items():
        g,d,a = traverse(v)
        groups += g
        ds += d
        attrs += a
    return groups,ds,attrs

def main(bundle):
    print(traverse(bundle['/']))
