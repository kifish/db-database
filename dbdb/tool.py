
def main(argv):
    if not (4 <= len(argv) <= 5): #变量检查
        usage()
        return BAD_ARGS

    dbname,verb,key,value = (argv[1:] + [None])[:4] #若len(argv) == 4，补None
    if verb not in {'get','set','delete'}:
        usage()
        return BAD_VERB

    db = dbdb.connect(dbname) # connect
    try:
        if verb == 'get':
            sys.stdout.write(db[key]) # get value and output
        elif verb == 'set':
            db[key] = value
            db.commit()
        else:  #delete
            del db[key]
            db.commit()
    except KeyError: # try中的三个分支 都涉及key
        print("Key not found",file = sys.stderr)
        return BAD_KEY
    return OK
    


def usage():
    pass
