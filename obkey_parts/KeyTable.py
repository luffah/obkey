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

import copy
from obkey_parts.Gui import AUTOMATIC
from obkey_parts.Gui import (
        Gtk, SensCondition, SensSwitcher,
        TYPE_UINT, TYPE_INT, TYPE_STRING, TYPE_BOOLEAN, TYPE_PYOBJECT
)
from obkey_parts.Resources import res, _
from obkey_parts.KeyUtils import key_openbox2gtk, key_gtk2openbox
from obkey_parts.OBKeyboard import OBKeyBind, OBKeyboard

# ======================================================== =
# KeyTable
# =========================================================


class KeyTable:
    """KeyTable"""

    def __init__(self, actionlist, obconfig):
        """__init__

        :param actionlist:
        :param ob:
        """
        self.widget = Gtk.VBox()
        self.ob = obconfig
        if obconfig.keyboard_node:
            self.keyboard = OBKeyboard(obconfig.keyboard_node)
        self.actionlist = actionlist
        actionlist.set_callback(self.actions_cb)

        self.icons = self.load_icons()

        self.model, self.cqk_model = self._create_models()
        self.view, self.cqk_view = self._create_views(
            self.model, self.cqk_model)

        # copy & paste
        self.copied = None

        # sensitivity switchers & conditions
        self.cond_insert_child = SensCondition(False)
        self.cond_paste_buffer = SensCondition(False)
        self.cond_selection_available = SensCondition(False)

        self.sw_insert_child_and_paste = SensSwitcher(
            [self.cond_insert_child,
             self.cond_paste_buffer])
        self.sw_insert_child = SensSwitcher(
            [self.cond_insert_child])
        self.sw_paste_buffer = SensSwitcher(
            [self.cond_paste_buffer])
        self.sw_selection_available = SensSwitcher(
            [self.cond_selection_available])

        self.context_menu = self._create_context_menu()

        for kb in self.keyboard.keybinds:
            self.apply_keybind(kb)

        self.apply_cqk_initial_value()

        # self.add_child_button
        self.widget.pack_start(self._create_toolbar(),
                               False, True, 0)
        self.widget.pack_start(self._create_scroll(self.view),
                               True, True, 0)
        self.widget.pack_start(self._create_cqk_hbox(self.cqk_view),
                               False, True, 0)

        if len(self.model):
            self.view.get_selection().select_iter(self.model.get_iter_first())

        self.sw_insert_child_and_paste.notify()
        self.sw_insert_child.notify()
        self.sw_paste_buffer.notify()
        self.sw_selection_available.notify()

    def _create_cqk_hbox(self, cqk_view):
        """_create_cqk_hbox

        :param cqk_view:
            """
        cqk_hbox = Gtk.HBox()
        cqk_label = Gtk.Label(label=_("chainQuitKey:"))
        cqk_label.set_padding(5, 5)

        cqk_frame = Gtk.Frame()
        cqk_frame.add(cqk_view)

        cqk_hbox.pack_start(cqk_label, False, False, False)
        cqk_hbox.pack_start(cqk_frame, True, True, 0)
        return cqk_hbox

    def _create_context_menu(self):
        """_create_context_menu"""
        context_menu = Gtk.Menu()
        self.context_items = {}

        item = Gtk.ImageMenuItem(Gtk.STOCK_CUT)
        item.connect('activate', lambda menu: self.cut_selected())
        item.get_child().set_label(_("Cut"))
        context_menu.append(item)
        self.sw_selection_available.append(item)

        item = Gtk.ImageMenuItem(Gtk.STOCK_COPY)
        item.connect('activate', lambda menu: self.copy_selected())
        item.get_child().set_label(_("Copy"))
        context_menu.append(item)
        self.sw_selection_available.append(item)

        item = Gtk.ImageMenuItem(Gtk.STOCK_PASTE)
        item.connect('activate',
                     lambda menu: self.insert_sibling(
                         copy.deepcopy(self.copied)))
        item.get_child().set_label(_("Paste"))
        context_menu.append(item)
        self.sw_paste_buffer.append(item)

        item = Gtk.ImageMenuItem(Gtk.STOCK_PASTE)
        item.get_child().set_label(_("Paste as child"))
        item.connect('activate',
                     lambda menu: self.insert_child(
                         copy.deepcopy(self.copied)))
        context_menu.append(item)
        self.sw_insert_child_and_paste.append(item)

        item = Gtk.ImageMenuItem(Gtk.STOCK_REMOVE)
        item.connect('activate',
                     lambda menu: self.del_selected())
        item.get_child().set_label(_("Remove"))
        context_menu.append(item)
        self.sw_selection_available.append(item)

        context_menu.show_all()
        return context_menu

    def _create_models(self):
        """_create_models"""
        model = Gtk.TreeStore(
            TYPE_UINT,     # accel key
            TYPE_INT,      # accel mods
            TYPE_STRING,   # accel string (openbox)
            TYPE_BOOLEAN,   # chroot
            TYPE_BOOLEAN,   # show chroot
            TYPE_PYOBJECT,  # OBKeyBind
            TYPE_STRING     # keybind descriptor
            )

        cqk_model = Gtk.ListStore(
                TYPE_UINT,    # accel key
                TYPE_INT,     # accel mods
                TYPE_STRING)  # accel string (openbox)
        return (model, cqk_model)

    def _create_scroll(self, view):
        """_create_scroll

        :param view:
            """
        scroll = Gtk.ScrolledWindow()
        scroll.add(view)
        scroll.set_policy(AUTOMATIC, AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        return scroll

    def _create_views(self, model, cqk_model):
        """_create_views

        :param model:
        :param cqk_model:
        """
        # added accel_mode=1 (CELL_RENDERER_ACCEL_MODE_OTHER) for key "Tab"
        r0 = Gtk.CellRendererAccel(accel_mode=1)
        r0.props.editable = True
        r0.connect('accel-edited', self.accel_edited)

        r1 = Gtk.CellRendererText()
        r1.props.editable = True
        r1.connect('edited', self.key_edited)

        r3 = Gtk.CellRendererText()
        r3.props.editable = False

        r2 = Gtk.CellRendererToggle()
        r2.connect('toggled', self.chroot_toggled)

        c0 = Gtk.TreeViewColumn(_("Key"), r0, accel_key=0, accel_mods=1)
        c1 = Gtk.TreeViewColumn(_("Key (text)"), r1, text=2)
        c2 = Gtk.TreeViewColumn(_("Chroot"), r2, active=3, visible=4)
        c3 = Gtk.TreeViewColumn(_("Action"), r3,  text=6)

        c0.set_resizable(True)
        c1.set_resizable(True)
        c2.set_resizable(True)
        c3.set_resizable(True)
        c0.set_fixed_width(200)
        c1.set_fixed_width(200)
        c2.set_fixed_width(100)
        c3.set_fixed_width(200)
        # the action column is the most important one,
        # so make it get the extra available space
        c3.set_expand(True)

        view = Gtk.TreeView(model)
        view.append_column(c3)
        view.append_column(c0)
        view.append_column(c1)
        view.append_column(c2)
        view.get_selection().connect('changed', self.view_cursor_changed)
        view.connect('button-press-event', self.view_button_clicked)

        # chainQuitKey table (wtf hack)

        r0 = Gtk.CellRendererAccel()
        r0.props.editable = True
        r0.connect('accel-edited', self.cqk_accel_edited)

        r1 = Gtk.CellRendererText()
        r1.props.editable = True
        r1.connect('edited', self.cqk_key_edited)

        c0 = Gtk.TreeViewColumn("Key", r0, accel_key=0, accel_mods=1)
        c1 = Gtk.TreeViewColumn("Key (text)", r1, text=2)

        def cqk_view_focus_lost(view, event):
            view.get_selection().unselect_all()

        cqk_view = Gtk.TreeView(cqk_model)
        cqk_view.set_headers_visible(False)
        cqk_view.append_column(c0)
        cqk_view.append_column(c1)
        cqk_view.connect('focus-out-event', cqk_view_focus_lost)
        return (view, cqk_view)

    def _create_toolbar(self):
        """_create_toolbar"""
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        toolbar.set_show_arrow(False)

        but = Gtk.ToolButton(Gtk.STOCK_SAVE)
        but.set_tooltip_text(_("Save ") + self.ob.path + _(" file"))
        but.connect('clicked', lambda b: self.ob.save(self.keyboard.deparse()))
        toolbar.insert(but, -1)

        toolbar.insert(Gtk.SeparatorToolItem(), -1)

        but = Gtk.ToolButton(Gtk.STOCK_DND_MULTIPLE)
        but.set_tooltip_text(_("Duplicate sibling keybind"))
        but.connect('clicked',
                    lambda b: self.duplicate_selected())
        toolbar.insert(but, -1)

        but = Gtk.ToolButton(Gtk.STOCK_COPY)
        but.set_tooltip_text(_("Copy"))
        but.connect('clicked',
                    lambda b: self.copy_selected())
        toolbar.insert(but, -1)

        toolbar.insert(Gtk.SeparatorToolItem(), -1)

        but = Gtk.ToolButton()
        but.set_icon_widget(self.icons['add_sibling'])
        but.set_tooltip_text(_("Insert sibling keybind"))
        but.connect('clicked',
                    lambda b: self.insert_sibling(
                        OBKeyBind()))
        toolbar.insert(but, -1)

        but = Gtk.ToolButton(Gtk.STOCK_PASTE)
        but.set_tooltip_text(_("Paste"))
        but.connect('clicked',
                    lambda b: self.insert_sibling(
                        copy.deepcopy(self.copied)))
        toolbar.insert(but, -1)

        toolbar.insert(Gtk.SeparatorToolItem(), -1)

        but = Gtk.ToolButton()
        but.set_icon_widget(self.icons['add_child'])
        but.set_tooltip_text(_("Insert child keybind"))
        but.connect('clicked',
                    lambda b: self.insert_child(
                        OBKeyBind()))
        toolbar.insert(but, -1)

        but = Gtk.ToolButton(Gtk.STOCK_PASTE)
        but.set_tooltip_text(_("Paste as child"))
        but.connect('clicked',
                    lambda b: self.insert_child(
                        copy.deepcopy(self.copied)))
        toolbar.insert(but, -1)

        toolbar.insert(Gtk.SeparatorToolItem(), -1)

        but = Gtk.ToolButton(Gtk.STOCK_REMOVE)
        but.set_tooltip_text(_("Remove keybind"))
        but.connect('clicked',
                    lambda b: self.del_selected())
        toolbar.insert(but, -1)
        self.sw_selection_available.append(but)

        sep = Gtk.SeparatorToolItem()
        sep.set_draw(False)
        sep.set_expand(True)
        toolbar.insert(sep, -1)

        toolbar.insert(Gtk.SeparatorToolItem(), -1)

        but = Gtk.ToolButton(Gtk.STOCK_QUIT)
        but.set_tooltip_text(_("Quit application"))
        but.connect('clicked',
                    lambda b: Gtk.main_quit())
        toolbar.insert(but, -1)
        return toolbar

    def apply_cqk_initial_value(self):
        """apply_cqk_initial_value"""
        cqk_accel_key, cqk_accel_mods = key_openbox2gtk(
            self.keyboard.chain_quit_key)
        if cqk_accel_mods == 0:
            self.keyboard.chain_quit_key = ""
        self.cqk_model.append((
            cqk_accel_key, cqk_accel_mods,
            self.keyboard.chain_quit_key))

    def get_action_desc(self, kb):
        """get_action_desc

        :param kb:
            """
        if len(kb.actions) > 0:
            if kb.actions[0].name == "Execute":
                frst_action = "[ "\
                    + kb.actions[0].options['command'] + " ]"
            elif kb.actions[0].name == "SendToDesktop":
                frst_action = _(kb.actions[0].name)\
                    + " " + str(kb.actions[0].options['desktop'])
            elif kb.actions[0].name == "Desktop":
                frst_action = _(kb.actions[0].name)\
                    + " " + str(kb.actions[0].options['desktop'])
            else:
                frst_action = _(kb.actions[0].name)
        else:
            frst_action = "."
        return frst_action

    def apply_keybind(self, kb, parent=None):
        """apply_keybind

        :param kb:
        :param parent:
        """
        accel_key, accel_mods = key_openbox2gtk(kb.key)
        chroot = kb.chroot
        show_chroot = len(kb.children) > 0 or not len(kb.actions)

        n = self.model.append(parent, (
            accel_key, accel_mods, kb.key,
            chroot, show_chroot, kb,
            self.get_action_desc(kb)))

        for c in kb.children:
            self.apply_keybind(c, n)

    def load_icons(self):
        """load_icons"""
        icons = {}
        icons['add_sibling'] = Gtk.Image.new_from_file(
                res.getIcon("add_sibling.png"))
        icons['add_child'] = Gtk.Image.new_from_file(
                res.getIcon("add_child.png"))
        return icons

    # ----------------------------------------------------------------------------
    # callbacks

    def view_button_clicked(self, view, event):
        """view_button_clicked

        :param view:
        :param event:
        """
        if event.button == 3:
            x = int(event.x)
            y = int(event.y)
            time = event.time
            pathinfo = view.get_path_at_pos(x, y)
            if pathinfo:
                path, col, cellx, celly = pathinfo
                view.grab_focus()
                view.set_cursor(path, col, 0)
                self.context_menu.popup(
                    None, None, None, None,
                    event.button, time)
            else:
                view.grab_focus()
                view.get_selection().unselect_all()
                self.context_menu.popup(
                    None, None, None, None,
                    event.button, time)
            return 1

    def actions_cb(self, val=None):
        """actions_cb

        :param val:
        """
        (model, it) = self.view.get_selection().get_selected()
        kb = model.get_value(it, 5)

        if len(kb.actions) == 0:
            model.set_value(it, 4, True)
            self.cond_insert_child.set_state(True)
        else:
            model.set_value(it, 6, self.get_action_desc(kb))
            model.set_value(it, 4, False)
            self.cond_insert_child.set_state(False)

    def view_cursor_changed(self, selection):
        """view_cursor_changed

        :param selection:
        """
        (model, it) = selection.get_selected()
        actions = None
        if it:
            kb = model.get_value(it, 5)
            if len(kb.children) == 0 and not kb.chroot:
                actions = kb.actions
            self.cond_selection_available.set_state(True)
            self.cond_insert_child.set_state(len(kb.actions) == 0)
        else:
            self.cond_insert_child.set_state(False)
            self.cond_selection_available.set_state(False)
        self.actionlist.set_actions(actions)

    def cqk_accel_edited(self, cell, path, accel_key, accel_mods, keycode):
        """cqk_accel_edited

        :param cell:
        :param path:
        :param accel_key:
        :param accel_mods:
        :param keycode:
        """
        self.cqk_model[path][0] = accel_key
        self.cqk_model[path][1] = accel_mods
        kstr = key_gtk2openbox(accel_key, accel_mods)
        self.cqk_model[path][2] = kstr
        self.keyboard.chain_quit_key = kstr
        self.view.grab_focus()

    def cqk_key_edited(self, cell, path, text):
        """cqk_key_edited

        :param cell:
        :param path:
        :param text:
        """
        self.cqk_model[path][0], self.cqk_model[path][1] \
            = key_openbox2gtk(text)
        self.cqk_model[path][2] = text
        self.keyboard.chain_quit_key = text
        self.view.grab_focus()

    def accel_edited(self, cell, path, accel_key, accel_mods, keycode):
        """accel_edited

        :param cell:
        :param path:
        :param accel_key:
        :param accel_mods:
        :param keycode:
        """
        self.model[path][0] = accel_key
        self.model[path][1] = accel_mods
        kstr = key_gtk2openbox(accel_key, accel_mods)
        self.model[path][2] = kstr
        self.model[path][5].key = kstr

    def key_edited(self, cell, path, text):
        """key_edited

        :param cell:
        :param path:
        :param text:
        """
        self.model[path][0], self.model[path][1] = key_openbox2gtk(text)
        self.model[path][2] = text
        self.model[path][5].key = text

    def chroot_toggled(self, cell, path):
        """chroot_toggled

        :param cell:
        :param path:
        """
        self.model[path][3] = not self.model[path][3]
        kb = self.model[path][5]
        kb.chroot = self.model[path][3]
        if kb.chroot:
            self.actionlist.set_actions(None)
        elif not kb.children:
            self.actionlist.set_actions(kb.actions)

    # -------------------------------------------------------------------------
    def cut_selected(self):
        """cut_selected"""
        self.copy_selected()
        self.del_selected()

    def duplicate_selected(self):
        """duplicate_selected"""
        self.copy_selected()
        self.insert_sibling(copy.deepcopy(self.copied))

    def copy_selected(self):
        """copy_selected"""
        (model, it) = self.view.get_selection().get_selected()
        if it:
            sel = model.get_value(it, 5)
            self.copied = copy.deepcopy(sel)
            self.cond_paste_buffer.set_state(True)

    def _insert_keybind(self, keybind, parent=None, after=None):
        """_insert_keybind

        :param keybind:
        :param parent:
        :param after:
        """
        keybind.parent = parent
        if parent:
            kbs = parent.children
        else:
            kbs = self.keyboard.keybinds

        if after:
            kbs.insert(kbs.index(after) + 1, keybind)
        else:
            kbs.append(keybind)

    def insert_sibling(self, keybind):
        """insert_sibling

        :param keybind:
        """
        (model, it) = self.view.get_selection().get_selected()

        accel_key, accel_mods = key_openbox2gtk(keybind.key)
        show_chroot = len(keybind.children) > 0 or not len(keybind.actions)

        if it:
            parent_it = model.iter_parent(it)
            parent = None
            if parent_it:
                parent = model.get_value(parent_it, 5)
            after = model.get_value(it, 5)

            self._insert_keybind(keybind, parent, after)
            newit = self.model.insert_after(
                parent_it, it, (
                    accel_key, accel_mods, keybind.key,
                    keybind.chroot, show_chroot,
                    keybind,
                    self.get_action_desc(keybind)))
        else:
            self._insert_keybind(keybind)
            newit = self.model.append(None, (
                accel_key, accel_mods, keybind.key,
                keybind.chroot, show_chroot,
                keybind,
                self.get_action_desc(keybind)))

        if newit:
            for c in keybind.children:
                self.apply_keybind(c, newit)
            self.view.get_selection().select_iter(newit)

    def insert_child(self, keybind):
        """insert_child

        :param keybind:
        """
        (model, it) = self.view.get_selection().get_selected()
        parent = model.get_value(it, 5)
        self._insert_keybind(keybind, parent)

        accel_key, accel_mods = key_openbox2gtk(keybind.key)
        show_chroot = len(keybind.children) > 0 or not len(keybind.actions)
#         newit =
        self.model.append(it, (
            accel_key, accel_mods, keybind.key,
            keybind.chroot, show_chroot, keybind,
            self.get_action_desc(keybind)))

#         if newit:
#             for c in keybind.children:
#                 self.apply_keybind(c, newit)
#             self.view.get_selection().select_iter(newit)
        # it means that we have inserted first child here, change status
        if len(parent.children) == 1:
            self.actionlist.set_actions(None)

    def del_selected(self):
        """del_selected"""
        (model, it) = self.view.get_selection().get_selected()
        if it:
            kb = model.get_value(it, 5)
            kbs = self.keyboard.keybinds
            if kb.parent:
                kbs = kb.parent.children
            kbs.remove(kb)
            isok = self.model.remove(it)
            if isok:
                self.view.get_selection().select_iter(it)
