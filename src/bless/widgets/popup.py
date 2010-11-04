from bless._widget import Widget

class Popup(Widget):
    def __init__(self, str):
        self.text = str.split('\n')
        height = len(self.text) + 4
        width = max([len(x) for x in self.text]) + 4
        super(Popup, self).__init__(height, width)

    def refresh(self):
        super(Popup, self).refresh()
        for (i, s) in enumerate(self.text):
            self.addstr(s, 2+i, 2)
