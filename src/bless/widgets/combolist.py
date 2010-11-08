from bless._widget import Widget
import bless.events

class ComboList(Widget):
    list = []
    pos = None

    def __init__(self, alignment=Widget.JUSTIFY_LEFT):
        super(ComboList, self).__init__()
        self.ehandler.define(bless.events.KEYS.UP, self.prev)
        self.ehandler.define(bless.events.KEYS.DOWN, self.next)
        self.alignment = alignment

    def __get_wrapped_str(self, str=None):
        def head(str):
            if self.alignment == self.JUSTIFY_LEFT:
                return " "
            elif self.alignment == self.JUSTIFY_CENTER:
                return " " * (self.width - len(str)) / 2

        def tail(str):
            return " " * (self.width - len(head(str)) - len(str))

        if not str: str = self.get_selected()
        return head(str) + str + tail(str)

    def add_item(self, str):
        self.list.append(str)
        self.pos = 0
        return len(self.list) - 1

    def get_selected(self):
        return self.list[self.pos]

    def jump(self, n):
        self.pos += n
        self.pos %= len(self.list)

    def next(self): self.jump(+1)
    def prev(self): self.jump(-1)

    def refresh(self):
        super(ComboList, self).refresh()
        for (i, item) in enumerate(self.list):
            if i >= self.height: break
            if len(item) > self.width:
                str = item[:self.width]
            else:
                str = item

            if i == self.pos:
                self.addstr(self.__get_wrapped_str(), self.pos, standout=1)
            else:
                self.addstr(self.__get_wrapped_str(str), i, 0)

