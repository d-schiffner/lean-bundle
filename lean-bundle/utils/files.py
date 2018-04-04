import time
from os import fstat
from .console import update_line

def linecount(file):
    # Really fast line counting!
    # Much faster than open as text and with buffering
    count = 0
    start = time.monotonic()
    with open(file, 'rb', buffering=0) as thefile:
        filesize = fstat(thefile.fileno()).st_size
        bytes_read = 0
        update_line("Reading line count in source file: 0 /", filesize)
        while True:
            #read 1mb chunks
            buffer = thefile.read(1048576)
            bytes_read += 1048576
            cur = time.monotonic()
            if (cur - start) > .05:
                update_line("Reading line count in source file:", bytes_read, '/', filesize)
                start = cur
            if not buffer:
                break
            count += buffer.count(b'\n')
        #clear the line
        update_line("File has {} lines".format(count))
        print('')
        return count
