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
from StringIO import StringIO
from os import system
from obkey_parts.XmlUtils import minidom, xml_find_node, fixed_writexml, parseString

class OpenboxConfig:
    """OpenboxConfig"""

    def __init__(self):
        self.dom = None
        self.keyboard = None
        self.path = None

    def load(self, path):
        self.path = path

        # load config DOM
        self.dom = minidom.parse(path)

        # try load keyboard DOM
        self.keyboard_node = xml_find_node(self.dom.documentElement, "keyboard")

    def save(self, keyboard_node):
        if self.path is None:
            return

        # it's all hack, waste of resources etc, but does pretty good result
        writer = StringIO()
        fixed_writexml(keyboard_node, writer,  "  ", "  ", "\n")

        newdom = xml_find_node(parseString(writer.getvalue()), "keyboard")
        keyboard = xml_find_node(self.dom.documentElement, "keyboard")
        self.dom.documentElement.replaceChild(newdom, keyboard)
        f = file(self.path, "w")
        if f:
            xmlform = self.dom.documentElement
            f.write(xmlform.toxml("utf8"))
            f.close()
        self.reconfigure_openbox()

    def reconfigure_openbox(self):
        system("openbox --reconfigure")
