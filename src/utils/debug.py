import os
import sys

try: os.mkdir("logs")
except OSError: pass

executable_name = os.path.basename(sys.argv[0])
logfile = open("logs/" + executable_name + "-debug", "w")
sys.stderr = open("logs/" + executable_name + "-stderr", "w")
level = 0


def ANNOTATE_DEBUG(fn):
    """
    This decorator logs the name, arguments and return value
    """

    def wrapper(*args, **kwargs):
        global level
        global logfile
        print >> logfile, "->" * level, "=== " + fn.__name__ + " ==="
        print >> logfile, "->" * level, args, kwargs
        level += 1
        fn_ret = fn(*args, **kwargs)
        level -= 1
        print >> logfile, "->" * level, fn_ret
        print >> logfile, "->" * level
        return fn_ret
    return wrapper

def DEBUG(s):
    print >> logfile, "==" * level, s
