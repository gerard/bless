#!/usr/bin/env python
from bless.widgets.combolist import ComboList
from bless.widgets.popup import Popup
from bless.application import Application
from bless.events import KEYS
import sys


def combo_selected(w):
    text = w.get_selected()
    popup = Popup(text)
    popup.set_titlebar(text)

    global app
    app.push(popup)
    app.handle()


combo = ComboList(['ASDF', 'QWER', 'ZXCV'])
combo.add_handler(KEYS.ENTER, combo_selected)
combo.set_titlebar("BLESS Test Application: %s" % sys.argv[0])

app = Application()
app.push(combo)
app.handle()
