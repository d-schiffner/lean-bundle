class LeanGroup():
    def __init__(self, backend, name):
        self.backend = backend
        self.attrs = {}
        self.name = name
    
    def __getitem__(self, x):
        if not path.isabs(x):
            x = path.abspath(path.join(self.name, x))
        return self.backend[x]
    
    def __getstate__(self):
        d = dict()
        d['name'] = self.name
        d['attrs'] = self.attrs.copy()
        return d
    
    def __getattr__(self, x):
        pass

    def create_group(self, name):
        return self.backend[name]

    def require_group(self, name):
        return self.backend[name]