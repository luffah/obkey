"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
"""
try:
    import gi
    gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
    from gi.repository import Gtk,Gdk
    from gi.repository.GObject import (TYPE_UINT, TYPE_INT,
                                       TYPE_BOOLEAN,
                                       TYPE_PYOBJECT,
                                       TYPE_STRING)
    from gi.repository.Gtk import AttachOptions, PolicyType
    (NEVER, AUTOMATIC, FILL, EXPAND) = (
            PolicyType.NEVER,
            PolicyType.AUTOMATIC,
            AttachOptions.FILL,
            AttachOptions.EXPAND)
except ImportError:
    print("Gtk 3.0 is required to run obkey.")
    exit

# =========================================================
# This is the uber cool switchers/conditions(sensors) system.
# Helps a lot with widgets sensitivity.
# =========================================================


class SensCondition:

    def __init__(self, initial_state):
        """__init__

        :param initial_state:
            """
        self.switchers = []
        self.state = initial_state

    def register_switcher(self, sw):
        """register_switcher

        :param sw:
        """
        self.switchers.append(sw)

    def set_state(self, state):
        """set_state

        :param state:
        """
        if self.state == state:
            return
        self.state = state
        for sw in self.switchers:
            sw.notify()


class SensSwitcher:

    def __init__(self, conditions):
        """__init__

        :param conditions:
            """
        self.conditions = conditions
        self.widgets = []

        for c in conditions:
            c.register_switcher(self)

    def append(self, widget):
        """append

        :param widget:
            """
        self.widgets.append(widget)

    def set_sensitive(self, state):
        """set_sensitive

        :param state:
            """
        for w in self.widgets:
            w.set_sensitive(state)

    def notify(self):
        """notify"""
        for c in self.conditions:
            if not c.state:
                self.set_sensitive(False)
                return
        self.set_sensitive(True)
