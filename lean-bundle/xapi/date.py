import iso8601

def timestamp(xapi, key):
    if key in xapi.statement:
        #stored as iso601 string
        return iso8601.parse_date(xapi.statement[key]).timestamp()
    elif key in xapi:
        #stored in $date key here
        return iso8601.parse_date(xapi[key]['$date']).timestamp()
    raise AttributeError("Key {} not in list of xapi statements".format(key))
