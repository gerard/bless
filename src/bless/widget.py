import curses
import time
import bless.events
from bless._event_handler import EventHandler
from utils.debug import DEBUG
from utils.bassert import ASSERT_SCREEN

class Widget(object):
    """
    Base Widget class
    """

    JUSTIFY_LEFT = 0
    JUSTIFY_CENTER = 1

    visible = False
    titlebar_str = ""
    statusbar_str = ""
    s = None

    def __init__(self, height=0, width=0):
        """
        Window independant initialization
        """

        if height != 0: height += 2
        if width  != 0: width += 2
        self.ysize = height
        self.xsize = width
        self.ehandler = EventHandler()

        # These events are ignored by default
        self.ehandler.define(bless.events.KEYS.UP)
        self.ehandler.define(bless.events.KEYS.DOWN)
        self.ehandler.define(bless.events.KEYS.RIGHT)
        self.ehandler.define(bless.events.KEYS.LEFT)


    def __screen_init__(self, yparent, xparent, yoff=0, xoff=0):
        """
        Window initialization
        """

        yparent -= yoff
        xparent -= xoff
        self.yoff = yoff
        self.xoff = xoff

        if self.ysize == 0 or self.xsize == 0:
            (self.yfitted, self.xfitted) = (yparent, xparent)
        else:
            self.yfitted = min(self.ysize, yparent)
            self.xfitted = min(self.xsize, xparent)

        self.s = curses.newwin(self.yfitted, self.xfitted, yoff, xoff)
        ystart = (yparent - self.yfitted) / 2
        xstart = (xparent - self.xfitted) / 2
        self.mvwin(ystart + self.yoff, xstart - self.yoff)

        self.s.border()
        self.s.keypad(1)

        (self.height, self.width) = (self.yfitted - 2, self.xfitted - 2)

    @ASSERT_SCREEN
    def __screen_del__(self):
        del(self.s)
        self.s = None

    def set_titlebar(self, str):
        self.titlebar_str = " " + str + " "

    def set_statusbar(self, str):
        self.statusbar_str = " " + str + " "

    @ASSERT_SCREEN
    def mvwin(self, y, x):
        return self.s.mvwin(y, x)

    @ASSERT_SCREEN
    def addstr(self, str, y, x=0, how=JUSTIFY_LEFT, attr=0, raw=0):
        if not raw:
            if x >= self.width: raise Exception
            if y >= self.height: raise Exception

        if how == self.JUSTIFY_CENTER:
            x = max(0, (self.width - len(str)) / 2)

        n = min(self.width - x, len(str))
        if not raw:
            self.s.addnstr(y+1, x+1, str, n, attr)
        else:
            self.s.addnstr(y, x, str, n, attr)

    @ASSERT_SCREEN
    def addch(self, c, y, x=0):
        self.s.addch(y+1, x+1, c)

    @ASSERT_SCREEN
    def refresh(self):
        self.s.border()
        self.addstr(self.titlebar_str, 0, how=self.JUSTIFY_CENTER, raw=1)
        self.addstr(self.statusbar_str, self.yfitted - 1, how=self.JUSTIFY_CENTER, raw=1)
        self.s.redrawwin()
        self.s.refresh()

    def add_handler(self, event, f=lambda: None, args=[]):
        return self.ehandler.define(event, f, [self] + args)

    def handle(self):
        while True:
            key = self.s.getch()
            if self.ehandler.is_defined(key):
                self.ehandler.run(key)
                self.refresh()
            else:
                return self.ehandler.run(key)

class Popup(Widget):
    def __init__(self, str):
        self.text = str.split('\n')

        height = len(self.text) + 4
        width = max([len(x) for x in self.text]) + 4
        super(Popup, self).__init__(height, width)


    @ASSERT_SCREEN
    def refresh(self):
        for (i, s) in enumerate(self.text):
            self.addstr(s, 2+i, 2)
        super(Popup, self).refresh()

class ComboList(Widget):
    def __init__(self, itemlist, init_pos = 0, how=Widget.JUSTIFY_LEFT):
        super(ComboList, self).__init__()
        self.list = itemlist
        self.how = how
        self.len = len(itemlist)
        self.pos = init_pos

        self.ehandler.define(bless.events.KEYS.UP, self.prev)
        self.ehandler.define(bless.events.KEYS.DOWN, self.next)

        self.jump(0)


    def __get_wrapped_str(self, str=None):
        def head(str):
            if self.how == self.JUSTIFY_LEFT:
                return " "
            elif self.how == self.JUSTIFY_CENTER:
                return " " * (self.width - len(str)) / 2

        def tail(str):
            return " " * (self.width - len(head(str)) - len(str))

        if not str: str = self.get_selected()
        return head(str) + str + tail(str)

    def get_selected(self):
        return self.list[self.pos]

    def jump(self, n):
        self.pos += n
        self.pos %= self.len

    def next(self): self.jump(+1)
    def prev(self): self.jump(-1)

    @ASSERT_SCREEN
    def refresh(self):
        super(ComboList, self).refresh()
        for (i, item) in enumerate(self.list):
            if i >= self.height: break
            if len(item) > self.width:
                str = item[:self.width]
            else:
                str = item

            if i == self.pos:
                self.addstr(self.__get_wrapped_str(), self.pos, attr=curses.A_STANDOUT)
            else:
                self.addstr(self.__get_wrapped_str(str), i, 0)


class TabContainer(Widget):
    def __init__(self):
        self.__tab_list = []

    def __screen_init__(self, yparent, xparent):
        super(TabContainer, self).__screen_init__(yparent, xparent)
        for w in self.__tab_list:
            w.__screen_init__(self, yparent, xparent, 2, 0)

    def __get_active_tab(self):
        return self.__tab_list[0]

    def __get_tab_names(self):
        return [name for (_, name) in self.__tab_list]

    def refresh(self):
        (w, _) = self.__get_active_tab()
        self.addstr(' | '.join(self.__get_tab_names))
        self.__get_active_widget()[0].refresh()

    def append(w, name):
        self.__tab_list.append((w, name))

    def jump(n):
        self.__tab_list = self.__tab_list[n:] + self.__tab_list[:n]


class Application:
    __widget_stack = []
    def __init__(self):
        self.s = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.s.keypad(1)
        (self.ysize, self.xsize) = self.s.getmaxyx()

    def __del__(self):
        self.s.keypad(0)
        self.s.erase()
        self.s.touchwin()
        self.s.refresh()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __get_widget(self):
        if self.__widget_stack == []: return None
        else: return self.__widget_stack[-1]

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
        """
        This only passes the control to the topmost widget
        """
        return self.__get_widget().handle()
