
class Writable(object):
    def sync(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            #don't write, if an exception occured
            return
        self.sync()
