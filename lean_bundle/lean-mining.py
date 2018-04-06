import os
import sys
from backend import *
from argparse import ArgumentParser
from types import ModuleType
from importlib import import_module

def add_script(bundle, src_file, script_name):
    src_file = os.path.abspath(src_file)
    if not os.path.exists(src_file):
        print("Failed to find", src_file)
        return
    basename = os.path.basename(src_file)
    basename,_ = os.path.splitext(basename)
    if not script_name:
        script_name = basename
    if script_name in bundle['/scripts']:
        print("Replacing code!!!")
    with open(src_file) as src_code:
        #TODO: Verify code!
        with LeanDataset(bundle['/scripts'], script_name) as lgd:
            lgd.data['code'] = src_code.read()
        print("Added script", src_file, 'to bundle', bundle.filename)

def run_script(bundle, script):
    if not script in bundle['/scripts']:
        print("Invalid script", script)
        print('Following scripts are known')
        return
    #get code
    code = bundle['/scripts/' + script].data['code']
    binary = compile(code, '/scripts/' + script, 'exec')
    #extend path
    sys.path.append(os.path.abspath(os.path.join(os.path.realpath(__file__),'..', '..')))
    tmp_env = {'LeanDataset' : LeanDataset, 'LeanGroup' : LeanGroup, 'LeanFile' : LeanFile, 'sys': sys}
    exec(binary, tmp_env)
    #run the code
    tmp_env['main'](bundle)

if __name__ == "__main__":
    parser = ArgumentParser("LeAn Mining")
    parser.add_argument('file', help="The LeAn file to work with")
    parser.add_argument('--add-script', help="The LeAnMining source to add")
    parser.add_argument('--script-name', default=None, help="Script alias")
    parser.add_argument('--run', help='Execute the given script')
    args = parser.parse_args()
    with LeanFile(args.file) as bundle:
        if args.add_script:
            add_script(bundle, args.add_script, args.script_name)
        if args.run:
            print("Executing script", args.run)
            run_script(bundle, args.run)
    print("Program finished")
