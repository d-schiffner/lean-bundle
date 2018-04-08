from backend import *
from argparse import ArgumentParser

def traverse(group, silent):
    if not silent:
        print(group)
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
        g,d,a = traverse(v, silent)
        groups += g
        ds += d
        attrs += a
    return groups,ds,attrs

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Dump")
    parser.add_argument('file')
    parser.add_argument('--silent', '-s', default=False, action='store_true')
    args = parser.parse_args()
    with LeanFile(args.file, 'r') as bundle:
        root = bundle['/']
        print(traverse(root, args.silent))
