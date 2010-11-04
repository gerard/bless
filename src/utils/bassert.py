def ASSERT_SCREEN(f):
    def wrapper(*args, **kwargs):
        if args[0].s == None:
            raise Exception
        else:
            return f(*args, **kwargs)
    return wrapper

def ASSERT_NOSCREEN(f):
    def wrapper(*args, **kwargs):
        if args[0].s != None:
            raise Exception
        else:
            return f(*args, **kwargs)
    return wrapper
