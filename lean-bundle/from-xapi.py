import h5py
import numpy as np
import sys
import json
from os import path
from argparse import ArgumentParser
from utils.json import JSONObject
from utils.group import LeanGroup
from utils.error import *
from xapi import actor, authority, date, lo, interaction


def add_statement(bundle, xapi):
    #read user
    statement = xapi.statement
    #print("Found statement: {} {} {}".format(statement.actor.name, statement.verb.id, statement.object.id))
    #create authority
    auth_grp = authority.get(bundle, statement)
    #create user group if not existing
    user_grp = actor.create_user(auth_grp, xapi.statement.actor)
    #TODO: how to identify configuration?
    config_grp = user_grp.require_group('general')
    #create timestamp entry
    time = str(date.timestamp(xapi, 'timestamp'))
    if time in config_grp:
        #this timestamp is already in here!
        #TODO: Sanity check!
        return
    fibers = config_grp.create_group(time)
    #create fibers
    interaction.create(fibers, bundle, statement)
    fibers.attrs.create('stored', date.timestamp(xapi,'stored'))
    if 'result' in statement:
        #TODO: Better parsing?
        LeanGroup(fibers).from_json(statement.result)
    #print("Statement added")

if __name__ == "__main__":
    print("Converting xAPI from JSON to LeAn Bundle")
    parser = ArgumentParser("LeAn Bundle xAPI Parser")
    parser.add_argument('--out')
    parser.add_argument('--replace', '-r', help="Replace the file with the new content", action='store_true')
    parser.add_argument('--skip', default=0, help="Skip the first x entries", type=int)
    parser.add_argument('--limit', default=None, help="Limit to x entries", type=int)
    parser.add_argument('file', help="The file to read the xAPI Statements from")

    args = parser.parse_args()
    if not args.out:
        #guess filename
        base, _ = path.splitext(args.file)
        args.out = base + '.lean'
    print("Creating file {}".format(args.out))
    if(args.replace):
        print("Replacing content in bundle")
        f = h5py.File(args.out, 'w')
    else:
        print("Appending to existing bundle")
        f = h5py.File(args.out)
    print("Reading line count in source file", end='\r')
    num_lines = sum(1 for line in open(args.file))
    if args.limit:
        num_lines = min(num_lines, args.limit)
    #clear the line
    print('                                 ', end='\r')
    with open(args.file, 'r') as data_file:
        count = 0
        for line in data_file:
            count += 1
            if count < args.skip:
                continue
            if args.limit and count > args.limit:
                break
            print("\x1b[2K\rStatement {} / {}".format(count, num_lines), end="")
            xapi = json.loads(line, object_hook=JSONObject)
            if 'statement' in xapi:
                try:
                    add_statement(f, xapi)
                except Exception as e:
                    import traceback
                    #print empty line to preserve counter
                    print('')
                    print(count)
                    print(e)
                    traceback.print_exc()
                    print(xapi)
                    if not isinstance(e, MissingConverterError):
                        sys.exit(1)
            else:
                print("No statement in line {}".format(count))
        print('')
    f.close()
    print("Program finished")