def get(statement):
    if 'authority' in statement and 'name' in statement.authority:
        #NOTE: We do not seem to use them correctly ...
        return statement.authority.name
    else:
        return 'anon'
