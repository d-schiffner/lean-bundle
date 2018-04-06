from backend import *
from argparse import ArgumentParser

def traverse(group):
    print(group)
    for k,v in group.items():
        print(v)
        print(v.keys())
        if isinstance(v, LeanGroup):
            traverse(v)

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Dump")
    parser.add_argument('file')
    args = parser.parse_args()
    with LeanFile(args.file) as bundle:
        traverse(bundle['/'])
