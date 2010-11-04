import curses

class KEYS_enum:
    ENTER = ord('\n')
    BACK = curses.KEY_BACKSPACE

    LEFT = curses.KEY_LEFT
    RIGHT = curses.KEY_RIGHT
    UP = curses.KEY_UP
    DOWN = curses.KEY_DOWN

    def __init__(self): pass

KEYS = KEYS_enum()
