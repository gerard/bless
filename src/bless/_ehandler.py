import bless.events

class EventHandler(object):
    __true_evs = [bless.events.KEYS.ENTER]

    def __init__(self):
        self.__edict = {}

    def __ev2bool(self, ev):
        return ev in self.__true_evs

    def is_defined(self, ev):
        return ev in self.__edict

    def define(self, ev, f=lambda: None, args=[]):
        self.__edict[ev] = (f, args)

    def run(self, ev):
        if ev in self.__edict:
            (f, args) = self.__edict[ev]
            return f(*args)
        else:
            return self.__ev2bool(ev)
