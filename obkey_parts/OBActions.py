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
from obkey_parts.XmlUtils import *
from obkey_parts.Gui import *
import copy

class OBAction:

    def __init__(self, name=None):
        self.options = {}
        self.option_defs = []
        self.name = name
        if name:
            self.mutate(name)

    def parse(self, dom):
        # call parseChild if childNodes exist
        if dom.hasChildNodes():
            for child in dom.childNodes:
                self.parseChild(child)

        # parse 'name' attribute, get options hash and parse
        self.name = dom.getAttribute("name")

        try:
            self.option_defs = actions[self.name]
        except KeyError:
            pass

        for od in self.option_defs:
            od.parse(self, dom)

    # calls itself until no childNodes are found
    # and strip() values of last node
    def parseChild(self, dom):
        try:
            if dom.hasChildNodes():
                for child in dom.childNodes:
                    try:
                        child.nodeValue = child.nodeValue.strip()
                    except AttributeError:
                        pass
                    self.parseChild(child)
        except AttributeError:
            pass
        else:
            try:
                dom.nodeValue = dom.nodeValue.strip()
            except AttributeError:
                pass

    def deparse(self):
        root = Element('action')
        root.setAttribute('name',str(self.name))
        for od in self.option_defs:
            od_node = od.deparse(self)
            if isinstance(od_node, list):
                for el in od_node:
                    root.appendChild(el)
            elif od_node:
                root.appendChild(od_node)
        return root

    def mutate(self, newtype):
        if (
                hasattr(self, "option_defs") and
                actions[newtype] == self.option_defs):
            self.options = {}
            self.name = newtype
            return

        self.options = {}
        self.name = newtype
        self.option_defs = actions[self.name]

        for od in self.option_defs:
            od.apply_default(self)

    def __deepcopy__(self, memo):
        # we need deepcopy here, because option_defs are never copied
        result = self.__class__()
        result.option_defs = self.option_defs
        result.options = copy.deepcopy(self.options, memo)
        result.name = copy.deepcopy(self.name, memo)
        return result

# =========================================================
# ActionList
# =========================================================
class ActionList:

    def __init__(self, proptable=None):
        self.widget = Gtk.VBox()
        self.actions = None
        self.proptable = proptable

        # actions callback, called when action added or deleted
        # for chroot possibility tracing
        self.actions_cb = None

        # copy & paste buffer
        self.copied = None

        # sensitivity switchers & conditions
        self.cond_paste_buffer = SensCondition(False)
        self.cond_selection_available = SensCondition(False)
        self.cond_action_list_nonempty = SensCondition(False)
        self.cond_can_move_up = SensCondition(False)
        self.cond_can_move_down = SensCondition(False)

        self.sw_paste_buffer = SensSwitcher([self.cond_paste_buffer])
        self.sw_selection_available = SensSwitcher(
            [self.cond_selection_available])
        self.sw_action_list_nonempty = SensSwitcher(
            [self.cond_action_list_nonempty])
        self.sw_can_move_up = SensSwitcher(
            [self.cond_can_move_up])
        self.sw_can_move_down = SensSwitcher(
            [self.cond_can_move_down])

        self.model = self.create_model()
        self.view = self.create_view(self.model)

        self.context_menu = self.create_context_menu()

        self.widget.pack_start(
            self.create_scroll(self.view),
                True, True, 0)
        self.widget.pack_start(
            self.create_toolbar(),
                False, True, 0)

        self.sw_paste_buffer.notify()
        self.sw_selection_available.notify()
        self.sw_action_list_nonempty.notify()
        self.sw_can_move_up.notify()
        self.sw_can_move_down.notify()

    def create_model(self):
        return Gtk.ListStore(TYPE_STRING, TYPE_PYOBJECT)

    def create_choices(self, ch):
        ret = ch
        actions_a = {}

        for a in actions_choices:
            actions_a[_(a)] = a
        for a in sorted(actions_a.keys()):
            actions_b = {}
            content_a = actions_choices[actions_a[a]]
            if (type(content_a) is dict):
                iter0 = ret.append(None, [a, ""])

                for b in content_a:
                    actions_b[_(b)] = b

                for b in sorted(actions_b.keys()):
                    actions_c = {}
                    content_b = content_a[actions_b[b]]
                    if (type(content_b) is dict):
                        iter1 = ret.append(
                            iter0, [b, ""])

                        for c in content_b:
                            actions_c[_(c)] = c
                        for c in sorted(actions_c.keys()):
                            ret.append(iter1, [c, actions_c[c]])

                    else:
                        ret.append(iter0, [b, actions_b[b]])
            else:
                ret.append(None, [a, actions_a[a]])

        return ret

    def create_scroll(self, view):
        scroll = Gtk.ScrolledWindow()
        scroll.add(view)
        scroll.set_policy(NEVER, AUTOMATIC)
        scroll.set_shadow_type(Gtk.ShadowType.IN)
        return scroll

    def create_view(self, model):
        renderer = Gtk.CellRendererCombo()

        def editingstarted(cell, widget, path):
            console.log('editing')
            widget.set_wrap_width(1)

        chs = Gtk.TreeStore(TYPE_STRING, TYPE_STRING)
        renderer.props.model = self.create_choices(chs)
        renderer.props.text_column = 0
        renderer.props.editable = True
        renderer.props.has_entry = False
        renderer.connect('changed', self.action_class_changed)
        renderer.connect('editing-started', editingstarted)

        column = Gtk.TreeViewColumn(_("Actions"), renderer, text=0)

        view = Gtk.TreeView(model)
        view.append_column(column)
        view.get_selection().connect('changed', self.view_cursor_changed)
        view.connect('button-press-event', self.view_button_clicked)
        return view

    def proptable_changed(self):
        if self.actions_cb:
            self.actions_cb()

    def create_context_menu(self):
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
        item.connect('activate', lambda menu: self.insert_action(self.copied))
        item.get_child().set_label(_("Paste"))
        context_menu.append(item)
        self.sw_paste_buffer.append(item)

        item = Gtk.ImageMenuItem(Gtk.STOCK_REMOVE)
        item.connect('activate', lambda menu: self.del_selected())
        item.get_child().set_label(_("Remove"))
        context_menu.append(item)
        self.sw_selection_available.append(item)

        context_menu.show_all()
        return context_menu

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        toolbar.set_style(Gtk.ToolbarStyle.ICONS)
        toolbar.set_icon_size(Gtk.IconSize.SMALL_TOOLBAR)
        toolbar.set_show_arrow(False)

        but = Gtk.ToolButton(Gtk.STOCK_ADD)
        but.set_tooltip_text(_("Insert action"))
        but.connect('clicked',
                    lambda b: self.insert_action(
                        OBAction("Execute")))
        toolbar.insert(but, -1)

        but = Gtk.ToolButton(Gtk.STOCK_REMOVE)
        but.set_tooltip_text(_("Remove action"))
        but.connect('clicked',
                    lambda b: self.del_selected())
        toolbar.insert(but, -1)
        self.sw_selection_available.append(but)

        but = Gtk.ToolButton(Gtk.STOCK_GO_UP)
        but.set_tooltip_text(_("Move action up"))
        but.connect('clicked',
                    lambda b: self.move_selected_up())
        toolbar.insert(but, -1)
        self.sw_can_move_up.append(but)

        but = Gtk.ToolButton(Gtk.STOCK_GO_DOWN)
        but.set_tooltip_text(_("Move action down"))
        but.connect('clicked',
                    lambda b: self.move_selected_down())
        toolbar.insert(but, -1)
        self.sw_can_move_down.append(but)

        sep = Gtk.SeparatorToolItem()
        sep.set_draw(False)
        sep.set_expand(True)
        toolbar.insert(sep, -1)

        but = Gtk.ToolButton(Gtk.STOCK_DELETE)
        but.set_tooltip_text(_("Remove all actions"))
        but.connect('clicked', lambda b: self.clear())
        toolbar.insert(but, -1)
        self.sw_action_list_nonempty.append(but)
        return toolbar
    # -----------------------------------------------------
    # callbacks

    def view_button_clicked(self, view, event):
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
                    None, None, None,
                        event.button, time, False)
            else:
                view.grab_focus()
                view.get_selection().unselect_all()
                self.context_menu.popup(
                    None, None, None,
                        event.button, time, False)
            return 1

    def action_class_changed(self, combo, path, it):
        m = combo.props.model
        ntype = m.get_value(it, 1)
        self.model[path][0] = m.get_value(it, 0)
        self.model[path][1].mutate(ntype)
        if self.proptable:
            self.proptable.set_action(self.model[path][1])
        if self.actions_cb :
            self.actions_cb()

    def view_cursor_changed(self, selection):
        (model, it) = selection.get_selected()
        act = None
        if it:
            act = model.get_value(it, 1)
        if self.proptable:
            self.proptable.set_action(act,self.proptable_changed)
        if act:
            nb = len(self.actions)
            i = self.actions.index(act)
            self.cond_can_move_up.set_state(i != 0)
            self.cond_can_move_down.set_state(nb > 1 and i + 1 < nb)
            self.cond_selection_available.set_state(True)
        else:
            self.cond_can_move_up.set_state(False)
            self.cond_can_move_down.set_state(False)
            self.cond_selection_available.set_state(False)

    # -----------------------------------------------------
    def cut_selected(self):
        self.copy_selected()
        self.del_selected()

    def duplicate_selected(self):
        self.copy_selected()
        self.insert_action(self.copied)

    def copy_selected(self):
        if self.actions is None:
            return

        (model, it) = self.view.get_selection().get_selected()
        if it:
            a = model.get_value(it, 1)
            self.copied = copy.deepcopy(a)
            self.cond_paste_buffer.set_state(True)

    def clear(self):
        if self.actions is None or not len(self.actions):
            return

        del self.actions[:]
        self.model.clear()

        self.cond_action_list_nonempty.set_state(False)
        if self.actions_cb:
            self.actions_cb()

    def move_selected_up(self):
        if self.actions is None:
            return

        (model, it) = self.view.get_selection().get_selected()
        if not it:
            return

        i, = self.model.get_path(it)
        nb = len(self.model)
        self.cond_can_move_up.set_state(i - 1 != 0)
        self.cond_can_move_down.set_state(nb > 1 and i < nb)
        if i == 0:
            return

        itprev = self.model.get_iter(i - 1)
        self.model.swap(it, itprev)
        action = self.model.get_value(it, 1)

        i = self.actions.index(action)
        tmp = self.actions[i - 1]
        self.actions[i - 1] = action
        self.actions[i] = tmp

    def move_selected_down(self):
        if self.actions is None:
            return

        (model, it) = self.view.get_selection().get_selected()
        if not it:
            return

        i, = self.model.get_path(it)
        nb = len(self.model)
        self.cond_can_move_up.set_state(i + 1 != 0)
        self.cond_can_move_down.set_state(nb > 1 and i + 2 < nb)
        if i + 1 >= nb:
            return

        itnext = self.model.iter_next(it)
        self.model.swap(it, itnext)
        action = self.model.get_value(it, 1)

        i = self.actions.index(action)
        tmp = self.actions[i + 1]
        self.actions[i + 1] = action
        self.actions[i] = tmp

    def insert_action(self, action):
        if self.actions is None:
            return

        (model, it) = self.view.get_selection().get_selected()
        if it:
            self._insert_action(action, model.get_value(it, 1))
            newit = self.model.insert_after(it, (_(action.name), action))
        else:
            self._insert_action(action)
            newit = self.model.append((_(action.name), action))

        if newit:
            self.view.get_selection().select_iter(newit)

        self.cond_action_list_nonempty.set_state(len(self.model))
        if self.actions_cb:
            self.actions_cb()

    def del_selected(self):
        if self.actions is None:
            return

        (model, it) = self.view.get_selection().get_selected()
        if it:
            self.actions.remove(model.get_value(it, 1))
            isok = self.model.remove(it)
            if isok:
                self.view.get_selection().select_iter(it)

        self.cond_action_list_nonempty.set_state(len(self.model))
        if self.actions_cb:
            self.actions_cb()

    # -----------------------------------------------------

    def set_actions(self, actionlist):
        self.actions = actionlist
        self.model.clear()
        self.widget.set_sensitive(self.actions is not None)
        if not self.actions:
            return
        for a in self.actions:
            self.model.append((_(a.name), a))

        if len(self.model):
            self.view.get_selection().select_iter(self.model.get_iter_first())
        self.cond_action_list_nonempty.set_state(len(self.model))

    def _insert_action(self, action, after=None):
        if after:
            self.actions.insert(self.actions.index(after) + 1, action)
        else:
            self.actions.append(action)

    def set_callback(self, cb):
        self.actions_cb = cb


# =========================================================
# MiniActionList
# =========================================================
class MiniActionList(ActionList):

    def __init__(self, proptable=None):
        ActionList.__init__(self, proptable)
        self.widget.set_size_request(-1, 120)
        self.view.set_headers_visible(False)

    def create_choices(self, ch):
        choices = ch
        action_list = {}
        for a in actions:
            action_list[_(a)] = a
        for a in sorted(action_list.keys()):
            if len(actions[action_list[a]]) == 0:
                choices.append((a, action_list[a]))
        return choices


# =========================================================
# Openbox Glue
# =========================================================

# Option Classes (for OBAction)
# 1. Parse function for OBAction to parse the data.
# 2. Getter(s) and Setter(s) for OBAction to operate on the data (registered by
# the parse function).
# 3. Widget generator for property editor to represent the data.
# Examples of such classes: string, int, filename, list of actions,
# list (choose one variant of many), string-int with custom validator(?)

# Actions
# An array of Options: <option_name> + <option_class>
# These actions are being applied to OBAction instances.


# =========================================================
# Option Class: String
# =========================================================
class OCString(object):
    __slots__ = ('name', 'default', 'alts')

    def __init__(self, name, default, alts=[]):
        self.name = name
        self.default = default
        self.alts = alts

    def apply_default(self, action):
        action.options[self.name] = self.default

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
        if not node:
            for a in self.alts:
                node = xml_find_node(dom, a)
                if node:
                    break
        if node:
            action.options[self.name] = xml_get_str(node)
        else:
            action.options[self.name] = self.default

    def deparse(self, action):
        val = action.options[self.name]
        if val == self.default:
            return None
        return parseString(
            "<" + str(self.name) + ">" +
                str(escape(val)) +
                "</" + str(self.name) + ">"
        ).documentElement

    def generate_widget(self, action, cb=None):
        def changed(entry, action):
            text = entry.get_text()
            action.options[self.name] = text
            if cb:
                cb()

        entry = Gtk.Entry()
        entry.set_text(action.options[self.name])
        entry.connect('changed', changed, action)
        return entry


# =========================================================
# Option Class: Combo
# =========================================================
class OCCombo(object):
    __slots__ = ('name', 'default', 'choices')

    def __init__(self, name, default, choices):
        self.name = name
        self.default = default
        self.choices = choices

    def apply_default(self, action):
        action.options[self.name] = self.default

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
        if node:
            action.options[self.name] = xml_get_str(node)
        else:
            action.options[self.name] = self.default

    def deparse(self, action):
        val = action.options[self.name]
        if val == self.default:
            return None
        return parseString(
            "<" + str(self.name) + ">" +
                str(val) +
                "</" + str(self.name) + ">"
        ).documentElement

    def generate_widget(self, action, cb=None):
        def changed(combo, action):
            text = combo.get_active()
            action.options[self.name] = self.choices[text]

        model = Gtk.ListStore(TYPE_STRING)
        for c in self.choices:
            model.append((_(c),))
        combo = Gtk.ComboBox()
        combo.set_active(self.choices.index(action.options[self.name]))
        combo.set_model(model)
        cell = Gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)
        combo.connect('changed', changed, action)
        return combo


# =========================================================
# Option Class: Number
# =========================================================
class OCNumber(object):
    __slots__ = ('name', 'default', 'min', 'max', 'explicit_defaults')

    def __init__(self, name, default, mmin, mmax, explicit_defaults=False):
        self.name = name
        self.default = default
        self.min = mmin
        self.max = mmax
        self.explicit_defaults = explicit_defaults

    def apply_default(self, action):
        action.options[self.name] = self.default

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
        if node:
            action.options[self.name] = int(float(xml_get_str(node)))
        else:
            action.options[self.name] = self.default

    def deparse(self, action):
        val = action.options[self.name]
        if not self.explicit_defaults and (val == self.default):
            return None
        return parseString(
            "<" + str(self.name) + ">" +
                str(val) +
                "</" + str(self.name) + ">"
        ).documentElement

    def generate_widget(self, action, cb=None):
        def changed(num, action):
            n = num.get_value_as_int()
            action.options[self.name] = n

        num = Gtk.SpinButton()
        num.set_increments(1, 5)
        num.set_range(self.min, self.max)
        num.set_value(action.options[self.name])
        num.connect('value-changed', changed, action)
        return num


# =========================================================
# Option Class: OCIf
#
# NO UI config yet
#
# Reason: keep manually defined IF key bindings
# =========================================================
class OCIf(object):
    __slots__ = ('name', 'default', 'props', 'then', 'els')

    def __init__(self, name, default):
        self.name = name
        self.default = default

        self.props = []
        self.then = []
        self.els = []

    def apply_default(self, action):
        action.options[self.name] = self.default

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
#         if dom.hasChildNodes():
        if node.hasChildNodes():
            for child in node.childNodes:
                if child.nodeName == "then":
                    self.then = self._parseAction(
                        node, action, "then")
                elif child.nodeName == "else":
                    self.els = self._parseAction(
                        node, action, "else")
                else:
                    if not isinstance(child,
                                      minidom.Text):
                        self.props += [child]

        def _parseAction(self, dom, action, nodeName):
            obAct = OCFinalActions()
            obAct.name = nodeName
            obAct.parse(action, dom)
            return obAct

    def deparse(self, action):
        frag = []

        # props
        for el in self.props:
            frag.append(el)

        # conditions
        # themEl = minidom.Element("then")
        themEl = self.then.deparse(action)
        themEl.tagName = "then"

        # else
        elseEl = self.els.deparse(action)
        elseEl.tagName = "else"

        frag.append(themEl)
        frag.append(elseEl)

        # print
        # zz = Element("action")
        # for el in frag:
        #     zz.appendChild(el)
        # print zz.toxml()

        return frag

    def generate_widget(self, action, cb=None):
        # label =
        Gtk.Label("IF Not fully supported yet")
        opts = []
        for el in self.props:
            opts.append({
                'name': "Cond.",
                "widget": Gtk.Label(el.toxml())
            })
        opts.append({
            'name': "then",
            "widget": self.then.generate_widget(action)
        })
        opts.append({
            'name': "else",
            'widget': self.els.generate_widget(action)
        })
        return opts


# =========================================================
# Option Class: Boolean
# =========================================================
class OCBoolean(object):
    __slots__ = ('name', 'default')

    def __init__(self, name, default):
        self.name = name
        self.default = default

    def apply_default(self, action):
        action.options[self.name] = self.default

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
        if node:
            action.options[self.name] = xml_parse_bool(node)
        else:
            action.options[self.name] = self.default

    def deparse(self, action):
        if action.options[self.name] == self.default:
            return None
        if action.options[self.name]:
            return parseString(
                "<" + str(self.name) +
                    ">yes</" + str(self.name) + ">"
            ).documentElement
        else:
            return parseString(
                "<" + str(self.name) +
                    ">no</" + str(self.name) + ">"
            ).documentElement

    def generate_widget(self, action, cb=None):
        def changed(checkbox, action):
            active = checkbox.get_active()
            action.options[self.name] = active

        check = Gtk.CheckButton()
        check.set_active(action.options[self.name])
        check.connect('toggled', changed, action)
        return check


# =========================================================
# Option Class: StartupNotify
# =========================================================
class OCStartupNotify(object):

    def __init__(self):
        self.name = "startupnotify"

    def apply_default(self, action):
        action.options['startupnotify_enabled'] = False
        action.options['startupnotify_wmclass'] = ""
        action.options['startupnotify_name'] = ""
        action.options['startupnotify_icon'] = ""

    def parse(self, action, dom):
        self.apply_default(action)

        startupnotify = xml_find_node(dom, "startupnotify")
        if not startupnotify:
            return

        enabled = xml_find_node(startupnotify, "enabled")
        if enabled:
            action.options['startupnotify_enabled'] = xml_parse_bool(enabled)
        wmclass = xml_find_node(startupnotify, "wmclass")
        if wmclass:
            action.options['startupnotify_wmclass'] = xml_get_str(wmclass)
        name = xml_find_node(startupnotify, "name")
        if name:
            action.options['startupnotify_name'] = xml_get_str(name)
        icon = xml_find_node(startupnotify, "icon")
        if icon:
            action.options['startupnotify_icon'] = xml_get_str(icon)

    def deparse(self, action):
        if not action.options['startupnotify_enabled']:
            return None
        root = parseString(
            "<startupnotify><enabled>yes</enabled></startupnotify>"
        ).documentElement
        if action.options['startupnotify_wmclass'] != "":
            root.appendChild(parseString(
                "<wmclass>" +
                action.options['startupnotify_wmclass'] +
                "</wmclass>"
            ).documentElement)
        if action.options['startupnotify_name'] != "":
            root.appendChild(parseString(
                "<name>" +
                action.options['startupnotify_name'] +
                "</name>"
            ).documentElement)
        if action.options['startupnotify_icon'] != "":
            root.appendChild(parseString(
                "<icon>" +
                action.options['startupnotify_icon'] +
                "</icon>"
            ).documentElement)
        return root

    def generate_widget(self, action, cb=None):
        def enabled_toggled(checkbox, action, sens_list):
            active = checkbox.get_active()
            action.options['startupnotify_enabled'] = active
            for w in sens_list:
                w.set_sensitive(active)

        def text_changed(textbox, action, var):
            text = textbox.get_text()
            action.options[var] = text

        wmclass = Gtk.Entry()
        wmclass.set_size_request(100, -1)
        wmclass.set_text(
            action.options['startupnotify_wmclass'])
        wmclass.connect(
            'changed', text_changed, action,
                'startupnotify_wmclass')

        name = Gtk.Entry()
        name.set_size_request(100, -1)
        name.set_text(action.options['startupnotify_name'])
        name.connect(
            'changed', text_changed, action,
                'startupnotify_name')

        icon = Gtk.Entry()
        icon.set_size_request(100, -1)
        icon.set_text(action.options['startupnotify_icon'])
        icon.connect(
            'changed', text_changed, action,
                'startupnotify_icon')

        sens_list = [wmclass, name, icon]

        enabled = Gtk.CheckButton()
        enabled.set_active(
            action.options['startupnotify_enabled'])
        enabled.connect(
            'toggled', enabled_toggled, action,
                sens_list)

        def put_table(table, label_text, widget, row, addtosens=True):
            label = Gtk.Label(label=_(label_text))
            label.set_padding(5, 5)
            label.set_alignment(0, 0)
            if addtosens:
                sens_list.append(label)
            table.attach(label, 0, 1, row, row + 1, EXPAND | FILL, 0, 0, 0)
            table.attach(widget, 1, 2, row, row + 1, FILL, 0, 0, 0)

        table = Gtk.Table(1, 2)
        put_table(table, "enabled:", enabled, 0, False)
        put_table(table, "wmclass:", wmclass, 1)
        put_table(table, "name:", name, 2)
        put_table(table, "icon:", icon, 3)

        sens = enabled.get_active()
        for w in sens_list:
            w.set_sensitive(sens)

        frame = Gtk.Frame()
        frame.add(table)
        return frame


# =========================================================
# Option Class: FinalActions
# =========================================================
class OCFinalActions(object):
    __slots__ = ('name')

    def __init__(self):
        self.name = "finalactions"

    def apply_default(self, action):
        a1 = OBAction()
        a1.mutate("Focus")
        a2 = OBAction()
        a2.mutate("Raise")
        a3 = OBAction()
        a3.mutate("Unshade")

        action.options[self.name] = [a1, a2, a3]

    def parse(self, action, dom):
        node = xml_find_node(dom, self.name)
        action.options[self.name] = []
        if node:
            for a in xml_find_nodes(node, "action"):
                act = OBAction()
                act.parse(a)
                action.options[self.name].append(act)
        else:
            self.apply_default(action)

    def deparse(self, action):
        a = action.options[self.name]
        if len(a) == 3:
            if (
                a[0].name == "Focus" and
                a[1].name == "Raise" and
                a[2].name == "Unshade"
            ):
                return None
        if len(a) == 0:
            return None
        root = parseString(
            "<finalactions/>").documentElement
        for act in a:
            node = act.deparse()
            root.appendChild(node)
        return root

    def generate_widget(self, action, cb=None):
        w = MiniActionList()
        w.set_actions(action.options[self.name])
        frame = Gtk.Frame()
        frame.add(w.widget)
        return frame


# ---------------------------------------------------------
actions_window_nav = {
    "NextWindow": [
        OCCombo('dialog', 'list', ['list', 'icons', 'none']),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCBoolean("allDesktops", False),
        OCBoolean("panels", False),
        OCBoolean("desktop", False),
        OCBoolean("linear", False),
        OCFinalActions()
    ],
    "PreviousWindow": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCBoolean("allDesktops", False),
        OCBoolean("panels", False),
        OCBoolean("desktop", False),
        OCBoolean("linear", False),
        OCFinalActions()
    ],
    "DirectionalFocusNorth": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusSouth": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusNorthEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusNorthWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusSouthEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalFocusSouthWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetNorth": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetSouth": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetNorthEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetNorthWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetSouthEast": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ],
    "DirectionalTargetSouthWest": [
        OCBoolean("dialog", True),
        OCBoolean("bar", True),
        OCBoolean("raise", False),
        OCFinalActions()
    ]
}
actions_desktop_nav_mov = {
    "Desktop": [
        OCNumber("desktop", 1, 1, 9999, True)
    ],
    "DesktopNext": [
        OCBoolean("wrap", True)
    ],
    "DesktopPrevious": [
        OCBoolean("wrap", True)
    ],
    "DesktopLeft": [
        OCBoolean("wrap", True)
    ],
    "DesktopRight": [
        OCBoolean("wrap", True)
    ],
    "DesktopUp": [
        OCBoolean("wrap", True)
    ],
    "DesktopDown": [
        OCBoolean("wrap", True)
    ],
    "GoToDesktop": [
        OCString("to", ""),
        OCString("wrap", "")
    ],
    "DesktopLast": []
}
actions_desktop_nav_del = {
    "RemoveDesktopLast": [],
    "RemoveDesktopCurrent": []
}
actions_desktop_nav_add = {
    "AddDesktopLast": [],
    "AddDesktopCurrent": []
}
actions_wm = {
    "ShowMenu": [OCString("menu", "")],
    "ToggleDockAutohide": [],
    "Reconfigure": [],
    "Restart": [
        OCString("command", "", ["execute"])
    ],
    "Exit": [
        OCBoolean("prompt", True)
    ],
    "SessionLogout": [
        OCBoolean("prompt", True)
    ],
    "Debug": [
        OCString("string", "")
    ],
    "ToggleShowDesktop": []
}
actions_window_focus = {
    "Focus": [],
    "Unfocus": [],
    "FocusToBottom": [],
    "RaiseLower": [],
    "Raise": [],
    "Lower": [],
    "ShadeLower": [],
    "UnshadeRaise": [],
    "ToggleAlwaysOnTop": [],
    "ToggleAlwaysOnBottom": [],
    "SendToTopLayer": [],
    "SendToBottomLayer": [],
    "SendToNormalLayer": []
}
actions_window_set = {
    "Iconify": [],
    "Close": [],
    "ToggleShade": [],
    "Shade": [],
    "Unshade": [],
    "ToggleOmnipresent": [],
    "ToggleMaximizeFull": [],
    "MaximizeFull": [],
    "UnmaximizeFull": [],
    "ToggleMaximizeVert": [],
    "MaximizeVert": [],
    "UnmaximizeVert": [],
    "ToggleMaximizeHorz": [],
    "MaximizeHorz": [],
    "UnmaximizeHorz": [],
    "ToggleFullscreen": [],
    "ToggleDecorations": [],
    "Decorate": [],
    "Undecorate": []
}

actions_window_send = {
    "SendToDesktop": [
        OCNumber("desktop", 1, 1, 9999, True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopNext": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopPrevious": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopLeft": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopRight": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopUp": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ],
    "SendToDesktopDown": [
        OCBoolean("wrap", True),
        OCBoolean("follow", True)
    ]
}
actions_window_move = {
    "Move": [],
    "MoveToCenter": [],
    "MoveResizeTo": [
        OCString("x", "current"),
        OCString("y", "current"),
        OCString("width", "current"),
        OCString("height", "current"),
        OCString("monitor", "current")
    ],
    "MoveRelative": [
        OCNumber("x", 0, -9999, 9999),
        OCNumber("y", 0, -9999, 9999)
    ],
    "MoveToEdgeNorth": [],
    "MoveToEdgeSouth": [],
    "MoveToEdgeWest": [],
    "MoveToEdgeEast": []
}
actions_window_resize = {
    "Resize": [
        OCCombo(
            "edge", "none", [
                'none', "top", "left", "right", "bottom",
                "topleft", "topright", "bottomleft",
                "bottomright"
            ])
    ],
    "ResizeRelative": [
        OCNumber("left", 0, -9999, 9999),
        OCNumber("right", 0, -9999, 9999),
        OCNumber("top", 0, -9999, 9999),
        OCNumber("bottom", 0, -9999, 9999)
    ],
    "GrowToEdgeNorth": [],
    "GrowToEdgeSouth": [],
    "GrowToEdgeWest": [],
    "GrowToEdgeEast": []
}

actions_choices = {
    "Execute": [
        OCString("command", "", ['execute']),
        OCString("prompt", ""),
        OCStartupNotify()
    ],
    # IF Not fully supported yet
    # "If": [ OCIf("", "") ],
    "BreakChroot": []
}

actions = {}
for k in actions_choices:
    actions[k] = actions_choices[k]
for k in actions_window_nav:
    actions[k] = actions_window_nav[k]
for k in actions_window_focus:
    actions[k] = actions_window_focus[k]
for k in actions_window_move:
    actions[k] = actions_window_move[k]
for k in actions_window_resize:
    actions[k] = actions_window_resize[k]
for k in actions_window_send:
    actions[k] = actions_window_send[k]
for k in actions_desktop_nav_add:
    actions[k] = actions_desktop_nav_add[k]
for k in actions_desktop_nav_del:
    actions[k] = actions_desktop_nav_del[k]
for k in actions_desktop_nav_mov:
    actions[k] = actions_desktop_nav_mov[k]
for k in actions_window_set:
    actions[k] = actions_window_set[k]
for k in actions_wm:
    actions[k] = actions_wm[k]

actions_choices["Window Navigation"] = actions_window_nav
actions_choices["Window Focus"] = actions_window_focus
actions_choices["Window Move"] = actions_window_move
actions_choices["Window Resize"] = actions_window_resize
actions_choices["Window Desktop Change"] = actions_window_send
actions_choices["Desktop Navigation"] = {
    "Add desktop": actions_desktop_nav_add,
 "Remove desktop": actions_desktop_nav_del,
 "Move to desktop": actions_desktop_nav_mov
}
actions_choices["Window Properties"] = actions_window_set
actions_choices["Window/Session Management"] = actions_wm

