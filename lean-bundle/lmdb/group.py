class LeanGroup(LeanBase):
    def __init__(self):
        super().__init__()
    
    def __getattr__(self, x):
        pass

    def create_group(self, name):
        pass

    def require_group(self, name):
        pass