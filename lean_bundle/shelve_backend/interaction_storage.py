
def interaction_storage(fibers, data):
    fibers.attrs['interaction_type'] = data[0].ref
    fibers.attrs['interaction_target'] = data[1].ref
