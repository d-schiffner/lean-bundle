class LeanGroup(LeanBase):
    def __init__(self):
        super().__init__()
    
    def __getattr__(self, x):
        pass
