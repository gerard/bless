import curses
from bless._ehandler import EventHandler

try:
    from utils.debug import DEBUG
except ImportError:
    def DEBUG(s): pass

class Application:
    __widget_stack = []
    def __init__(self):
        self.s = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.s.keypad(1)
        (self.ysize, self.xsize) = self.s.getmaxyx()

        self.ehandler = EventHandler()
        self.ehandler.define(curses.KEY_RESIZE, self.resize)
        self.ehandler.define(-1, lambda: None)

    def __del__(self):
        self.s.erase()
        self.s.refresh()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __get_widget(self):
        if self.__widget_stack == []: return None
        else: return self.__widget_stack[-1]

    def close(self):
        self.__del__()

    def resize(self):
        (newy, newx) = self.s.getmaxyx()
        for w in self.__widget_stack: w.resize(newy, newx, 0, 0)
        for w in self.__widget_stack: w.refresh()

    def push(self, w):
        """
        Push the widget to the application

        The widget window needs to be repositioned (for now, only centered),
        pushed to the widget stack and finally a refresh signal is given to it
        so it can draw itself.
        """
        self.__widget_stack.append(w)
        w.__screen_init__(self.ysize, self.xsize)
        w.refresh()

    def pop(self):
        """
        Remove the topmost window and delete it
        """
        ret = self.__widget_stack.pop()
        ret.__screen_del__()

        w = self.__get_widget()
        if w: w.refresh()

        return ret

    def handle(self):
        w = self.__get_widget()
        while True:
            key = w.s.getch()
            try:
                if self.ehandler.is_defined(key):
                    self.ehandler.run(key)
                else:
                    (again, ret) = w.handle(key)
                    w.refresh()
                    if not again: return ret
            except:
                self.__del__()
                raise
