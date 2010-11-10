import curses
import bless.events
from bless._ehandler import EventHandler

try:
    from utils.debug import DEBUG
    from utils.bassert import ASSERT_SCREEN
except ImportError:
    # These modules should not be available in the distribution.  Simply define
    # some dummy stubs for now.
    def DEBUG(s): pass
    def ASSERT_SCREEN(f): return f

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


    def __screen_fit(self, yparent, xparent):
        if self.ysize == 0 or self.xsize == 0:
            return (yparent, xparent)
        else:
            return (min(self.ysize, yparent), min(self.xsize, xparent))

    def __screen_position(self, yparent, xparent):
        ystart = (yparent - self.yfitted) / 2
        xstart = (xparent - self.xfitted) / 2
        return (ystart, xstart)

    def __screen_init__(self, yparent, xparent, yoff=0, xoff=0):
        """
        Window initialization
        """

        yparent -= yoff
        xparent -= xoff
        self.yoff = yoff
        self.xoff = xoff

        (self.yfitted, self.xfitted) = self.__screen_fit(yparent, xparent)
        self.s = curses.newwin(self.yfitted, self.xfitted, yoff, xoff)

        (ystart, xstart) = self.__screen_position(yparent, xparent)
        self.mvwin(ystart + self.yoff, xstart - self.xoff)

        (self.height, self.width) = (self.yfitted - 2, self.xfitted - 2)

        self.s.border()
        self.s.keypad(1)


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

    def resize(self, y, x, yoff=0, xoff=0):
        self.__screen_init__(y, x, yoff, xoff)
        self.refresh()

    @ASSERT_SCREEN
    def addstr(self, str, y, x=0, how=JUSTIFY_LEFT, standout=0, raw=0):
        if not raw:
            if x >= self.width: raise Exception
            if y >= self.height: raise Exception

        if how == self.JUSTIFY_CENTER:
            x = max(0, (self.width - len(str)) / 2)

        attr = 0
        if standout:
            attr = curses.A_STANDOUT

        n = min(self.width - x, len(str))
        try:
            if not raw:
                self.s.addnstr(y+1, x+1, str, n, attr)
            else:
                self.s.addnstr(y, x, str, n, attr)
        except curses.error:
            # Unfortunately, we have no way to tell if one resize event has just
            # happened and we are unable to control that we are not writing
            # outside the window.  It should be safe to ignore this error, as
            # a refresh will come with the resize event.
            pass

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

    def handle(self, key):
        if self.ehandler.is_defined(key):
            self.ehandler.run(key)
            self.s.refresh()
            return (True, None)
        else:
            return (False, self.ehandler.run(key))

