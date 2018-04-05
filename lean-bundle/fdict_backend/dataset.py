from os import path
from .base import LeanBase

class LeanDataset(LeanBase):
    def __init__(self, parent, name):
        pathname = path.join(parent.name, name)
        super().__init__(parent.backend, pathname)
        self.parent = parent
    
    def from_json(self, json):
        self.data.update(json.__dict__)
        return self
