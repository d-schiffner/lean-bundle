import os
from backend import *
from argparse import ArgumentParser
from types import ModuleType

def add_script(bundle, src_file):
    basename = os.path.basename(src_file)
    basename,_ = os.path.splitext(basename)
    with open(src_file) as src_code:
        #TODO: Verify code!
        bundle['/scripts']

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Mining")
    parser.add_argument('file', help="The LeAn file to work with")
    parser.add_argument('--script-src', help="The LeAnMining source to add")
    parser.add_argument('--run', 'Execute the given code')
    args = parser.parse_args()
    with LeanFile(args.file) as bundle:
        if(args.script_src and os.path.exists(args.script_src)):
            add_script(bundle, args.script_src)
        if(args.run and args.run in bundle['/scripts']):
            print("Executing script", args.run)
            run_script(bundle, args.run)
    print("Program finished")
