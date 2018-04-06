from lean-bundle.backend import *

def traverse(group):
    print(group)
    for k,v in group.items():
        print(v)
        if isinstance(v, LeanGroup):
            traverse(v)

def main(bundle):
    traverse(bundle['/'])