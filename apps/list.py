#!/usr/bin/env python
import bless.widget
import bless.events

combo_contents = [
    'ASDF',
    'QWER',
    'ZXCV',
]


def combo_selected(w):
    global app
    s = w.get_selected()
    popup = bless.widget.Popup(s)
    app.push(popup)
    app.handle()
    

app = bless.widget.Application()
combo = bless.widget.ComboList(combo_contents)
combo.add_handler(bless.events.KEYS.ENTER, combo_selected)
app.push(combo)
app.handle()
