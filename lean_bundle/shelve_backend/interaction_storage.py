
def interaction_storage(fibers, data):
    fibers.attrs['interaction_type'] = data[0]
    fibers.attrs['interaction_target'] = data[1]
