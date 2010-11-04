from bless._widget import Widget

class TabContainer(Widget):
    """
    TODO: Far from ready
    """

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

