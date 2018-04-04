import mmap
class LeanFile():
    def __init__(self, filename, mode):
        self.file = open(filename, mode+"b")
        self.mmap = mmap(self.file.fileno(), 1024**2)
        