"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
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
