"""
  This file is a part of Openbox Key Editor
  Copyright (C) 2009 nsf <no.smile.face@gmail.com>
  v1.1 - Code migrated from PyGTK to PyGObject
         github.com/stevenhoneyman/obkey
  v1.2pre  - 19.06.2016 - structured presentation of actions...
  v1.2     - 24.02.2018 - slightly refactored code - more dynamic
         github.com/luffah/obkey

  MIT License

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
"""

from obkey_parts.Resources import _
from obkey_parts.Gui import Gtk, NEVER, AUTOMATIC, EXPAND, FILL

# =========================================================
# PropertyTable
# =========================================================


class PropertyTable:

    def __init__(self):
        """__init__"""
        self.widget = Gtk.ScrolledWindow()
        self.table = Gtk.Table(1, 2)
        self.table.set_row_spacings(5)
        self.widget.add_with_viewport(self.table)
        self.widget.set_policy(NEVER, AUTOMATIC)

    def add_row(self, label_text, table):
        """add_row

        :param label_text:
        :param table:
        """
        label = Gtk.Label(label=_(label_text))
        label.set_alignment(0, 0)
        row = self.table.props.n_rows
        self.table.attach(
            label, 0, 1, row, row + 1,
            EXPAND | FILL,
            0, 5, 0)
        self.table.attach(table, 1, 2, row, row + 1, FILL, 0, 5, 0)

    def clear(self):
        """clear"""
        cs = self.table.get_children()
        cs.reverse()
        for c in cs:
            self.table.remove(c)
        self.table.resize(1, 2)

    def set_action(self, action, cb=None):
        """set_action

        :param action:
        :param cb:
        """
        self.clear()
        # label = Gtk.Label(label=_('Properties'))
        # label.set_alignment(0, 0)
        # row = self.table.props.n_rows
        # self.table.attach(
        # label, 0, 1, row, row + 1,
        # EXPAND | FILL,
        # 0, 5, 0)
        if not action:
            return
        for a in action.option_defs:
            widget = a.generate_widget(action, cb)
            # IF can return a list
            if isinstance(widget, list):
                for row in widget:
                    self.add_row(row['name'] + ":", row['widget'])
            else:
                self.add_row(a.name + ":", widget)
        self.table.queue_resize()
        self.table.show_all()


# event = gtk.gdk.Event(gtk.gdk.FOCUS_CHANGE)
# event.window = entry.get_window()  # the gtk.gdk.Window of the widget
# event.send_event = True  # this means you sent the event explicitly
# event.in_ = False  # False for focus out, True for focus in
