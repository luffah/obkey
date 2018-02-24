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
"""
   OBKeyBind class definition
   OBKeyboard is a collection of OBKeyBind + chainQuitKey
"""
from obkey_parts.OBActions import OBAction
from obkey_parts.XmlUtils import xml_find_nodes, xml_find_node, xml_get_str, parseString, Element


class OBKeyBind(object):
    """OBKeyBind"""

    def __init__(self, parent=None):
        self.children = []
        self.actions = []
        self.key = "a"
        self.chroot = False
        self.parent = parent

    def parse(self, dom):
        """parse

        :param dom:
        """
        self.key = dom.getAttribute("key")
        self.chroot = dom.getAttribute("chroot") in ['true', 'yes', 'on']

        kbinds = xml_find_nodes(dom, "keybind")
        if len(kbinds):
            for k in kbinds:
                keybind = OBKeyBind(self)
                keybind.parse(k)
                self.children.append(keybind)
        else:
            for action in xml_find_nodes(dom, "action"):
                newaction = OBAction()
                newaction.parse(action)
                self.actions.append(newaction)

    def deparse(self):
        """deparse"""
        root = Element('keybind')
        root.setAttribute('key', str(self.key))
        if self.chroot:
            root.setAttribute('chroot', "yes")
            # root = parseString(
                #'<keybind key="' +
                    # str(self.key) +
                # '" chroot="yes"/>').documentElement
        # else:
            # root = parseString(
            #    '<keybind key="' +
                    # str(self.key) +
            #        '"/>').documentElement

        if len(self.children):
            for keybind in self.children:
                root.appendChild(keybind.deparse())
        else:
            for action in self.actions:
                root.appendChild(action.deparse())
        return root

    # def insert_empty_action(self, after=None):
        """insert_empty_action

        :param after:
        """
        # newact = OBAction()
        # newact.mutate("Execute")

        # if after:
            # self.actions.insert(self.actions.index(after) + 1, newact)
        # else:
            # self.actions.append(newact)
        # return newact

    def move_up(self, action):
        """move_up

        :param action:
        """
        i = self.actions.index(action)
        tmp = self.actions[i - 1]
        self.actions[i - 1] = action
        self.actions[i] = tmp

    def move_down(self, action):
        """move_down

        :param action:
        """
        i = self.actions.index(action)
        tmp = self.actions[i + 1]
        self.actions[i + 1] = action
        self.actions[i] = tmp


class OBKeyboard(object):
    """OBKeyboard"""

    def __init__(self, dom):
        self.chain_quit_key = None
        self.keybinds = []

        cqk = xml_find_node(dom, "chainQuitKey")
        if cqk:
            self.chain_quit_key = xml_get_str(cqk)

        for keybind_node in xml_find_nodes(dom, "keybind"):
            keybind = OBKeyBind()
            keybind.parse(keybind_node)
            self.keybinds.append(keybind)

    def deparse(self):
        """deparse"""

        root = parseString('<keyboard/>').documentElement
        chain_quit_key_node = parseString('<chainQuitKey>' +
                                          str(self.chain_quit_key) +
                                          '</chainQuitKey>').documentElement
        root.appendChild(chain_quit_key_node)

        for k in self.keybinds:
            root.appendChild(k.deparse())

        return root
