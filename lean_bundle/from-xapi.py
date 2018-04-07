import sys
import json
import logging
import time
from os import path
from argparse import ArgumentParser
from utils.json import JSONObject
from utils.error import *
from utils.files import linecount
from utils.console import update_line
from xapi import actor, authority, date, lo, interaction, result, context

#multithreading
from queue import Queue
from threading import Thread

logging.basicConfig(level=logging.INFO)
#load the backend
from backend import *

def process_statement(bundle, xapi):
    log = logging.getLogger()
    if not 'statement' in xapi:
        xapi = JSONObject({'statement': xapi})
    #read user
    statement = xapi.statement
    log.debug("Found statement: {} {} {}".format(statement.actor.name, statement.verb.id, statement.object.id))
    #create authority
    auth_grp = authority.get(bundle, statement)
    #create user group if not existing
    user_grp = actor.create_user(auth_grp, statement.actor)
    #TODO: how to identify configuration?
    config_grp = user_grp.require_group('general')
    #create timestamp entry
    time = str(date.timestamp(xapi, 'timestamp'))
    #replace timestamp
    #NOTE: this is made to allow import from _dump.json files
    statement.timestamp = statement.timestamp if 'timestamp' in statement else xapi.timestamp
    if time in config_grp:
        #this timestamp is already in here!
        log.debug("Timestamp already exists")
        #TODO: Sanity check!
        if 'context' in statement and 'instructor' in statement.context:
            statement.context = {'instructor': statement.context.instructor}
        return statement
    fibers = config_grp.create_group(time)
    #create fibers
    #copy id
    fibers.attrs['id'] = statement.id
    interaction.create(fibers, statement)
    stored = date.timestamp(xapi,'stored')
    fibers.attrs.create('stored', stored)
    #replace stored
    #NOTE: this is made to allow import from _dump.json files
    statement.stored = statement.stored if 'stored' in statement else xapi.stored
    result.parse(fibers, statement)
    context.parse(auth_grp, fibers, statement)
    #bundle.sync()
    return statement

STATEMENT_QUEUE = Queue()
def writer_worker(dumpfile):
    i = 0
    with open(dumpfile, 'w') as xapidump:
        while True:
            entry = STATEMENT_QUEUE.get()
            if entry is None:
                break
            JSONObject.dump(entry, xapidump, separators=(',',':'))
            xapidump.write('\n')
            STATEMENT_QUEUE.task_done()
    print("Writer finished")
    STATEMENT_QUEUE.task_done()

if __name__ == "__main__":
    log = logging.getLogger()
    print("Converting xAPI from JSON to LeAn Bundle")
    parser = ArgumentParser("LeAn Bundle xAPI Parser")
    parser.add_argument('--out')
    parser.add_argument('--keep', '-k', help="Keep the file and extend with the new content", action='store_true')
    parser.add_argument('--skip', default=0, help="Skip the first x entries", type=int)
    parser.add_argument('--limit', default=None, help="Limit to x entries", type=int)
    parser.add_argument('--no-line-count', default=False, help="Skip counting lines", action="store_true")
    parser.add_argument('--dump', default=False, help="Prevent dump converted parts of the statements", action="store_true")
    parser.add_argument('file', help="The file to read the xAPI Statements from")
    parser.add_argument('-v', '--verbose', help="Verbose logging", action='store_true')
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug("Debugging enabled")
    
    if not args.out:
        #guess filename
        base, _ = path.splitext(args.file)
        args.out = base + '.lean'
    if args.dump:
        base, _ = path.splitext(args.out)
        args.dump = base + "_dump.json"
        if args.dump and path.exists(args.dump):
            import os
            os.remove(args.dump)
    num_lines = linecount(args.file) if not args.no_line_count else 0
    print("Creating file", args.out)
    if(args.keep):
        print("Appending to existing bundle")
        f = LeanFile(args.out)
    else:
        print("Replacing content in bundle")
        f = LeanFile(args.out, 'w')
    if args.limit:
        num_lines = min(num_lines, args.limit)
    #create default groups
    last = time.monotonic()
    #read statements
    with open(args.file, 'r') as data_file:
        if args.dump:
            writer_thread = Thread(target=writer_worker, args=(args.dump,))
            writer_thread.setDaemon(True)
            writer_thread.start()
        count = 0
        for line in data_file:
            count += 1
            if count < args.skip:
                continue
            if args.limit and count >= args.limit:
                break
            cur = time.monotonic()
            if not args.verbose and (cur - last) > .15:
                update_line("Statement", count, '/', num_lines)
                last = cur
            xapi = json.loads(line, object_hook=JSONObject)
            try:
                conv = process_statement(f, xapi)
                if args.dump:
                    STATEMENT_QUEUE.put(conv)
            except Exception as e:
                import traceback
                #print empty line to preserve counter
                print('')
                print(count)
                print(e)
                traceback.print_exc()
                #print(xapi)
                if not isinstance(e, MissingConverterError):
                    sys.exit(1)
        #complete line
        update_line("Statement", count, '/', num_lines)
        print('')
        #end writer thread
        if args.dump:
            print("Ending json writer thread")
            STATEMENT_QUEUE.put(None)
            STATEMENT_QUEUE.join()
        #close handles
    f.close()
    print("Program finished")
