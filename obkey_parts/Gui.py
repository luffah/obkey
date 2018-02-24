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
try:
    import gi
    gi.require_versions({'Gtk': '3.0', 'GLib': '2.0', 'Gio': '2.0'})
    from gi.repository import Gtk
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
    print "Gtk 3.0 is required to run obkey."
    exit

# =========================================================
# This is the uber cool switchers/conditions(sensors) system.
# Helps a lot with widgets sensitivity.
# =========================================================
class SensCondition:

    def __init__(self, initial_state):
        self.switchers = []
        self.state = initial_state

    def register_switcher(self, sw):
        self.switchers.append(sw)

    def set_state(self, state):
        if self.state == state:
            return
        self.state = state
        for sw in self.switchers:
            sw.notify()


class SensSwitcher:

    def __init__(self, conditions):
        self.conditions = conditions
        self.widgets = []

        for c in conditions:
            c.register_switcher(self)

    def append(self, widget):
        self.widgets.append(widget)

    def set_sensitive(self, state):
        for w in self.widgets:
            w.set_sensitive(state)

    def notify(self):
        for c in self.conditions:
            if not c.state:
                self.set_sensitive(False)
                return
        self.set_sensitive(True)


