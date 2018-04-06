import os
from backend import *
from argparse import ArgumentParser
from types import ModuleType

def add_script(bundle, src_file):
    src_file = os.path.abspath(src_file)
    if not os.path.exists(src_file):
        print("Failed to find", src_file)
        return
    basename = os.path.basename(src_file)
    basename,_ = os.path.splitext(basename)
    with open(src_file) as src_code:
        #TODO: Verify code!
        with LeanDataset(bundle['/scripts'], basename) as lgd:
            lgd.data['code'] = src_code.read()
        print("Added script", src_file, 'to bundle', bundle.filename)

def run_script(bundle, script):
    if not script in bundle['/scripts']:
        print("Invalid script", script)
        print('Following scripts are known')
        return
    #get code
    code = bundle['/scripts/' + script].data['code']
    binary = compile(code, '', 'exec')
    print(binary)

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Mining")
    parser.add_argument('file', help="The LeAn file to work with")
    parser.add_argument('--add-script', help="The LeAnMining source to add")
    parser.add_argument('--run', help='Execute the given script')
    args = parser.parse_args()
    with LeanFile(args.file) as bundle:
        if args.add_script:
            add_script(bundle, args.add_script)
        if args.run:
            print("Executing script", args.run)
            run_script(bundle, args.run)
    print("Program finished")
