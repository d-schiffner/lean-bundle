
def update_line(*args, **kwargs):
    #force kwargs end to be empty
    kwargs['end'] = ''
    message = '\x1b[2K\r{}'.format(' '.join([str(x) for x in args]))
    print(message, **kwargs)
