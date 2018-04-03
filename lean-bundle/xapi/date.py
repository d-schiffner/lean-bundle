import iso8601

def timestamp(xapi, key):
    if key in xapi.statement:
        #stored as iso601 string
        return int(iso8601.parse_date(xapi.statement[key]).timestamp()*10000)
    elif key in xapi:
        #stored in $date key here
        return int(iso8601.parse_date(xapi[key]['$date']).timestamp()*10000)
    raise ValueError("Key {} not in list of xapi statements".format(key))
