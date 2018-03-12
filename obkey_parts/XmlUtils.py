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
import xml.dom.minidom as minidom
from xml.dom.minidom import parseString, Element
from xml.sax.saxutils import escape


def xml_get_str(elt):
    """xml_get_str

    :param elt:XML element
    """
    return elt.firstChild.nodeValue if elt.hasChildNodes() else ""


def xml_parse_bool(elt):
    """xml_parse_bool

    :param elt:XML element
        """
    val = elt.firstChild.nodeValue.lower()
    if val == "true" or val == "yes" or val == "on":
        return True
    return False


def xml_find_nodes(elt, name):
    """xml_find_nodes

    :param elt:XML parent element
    :param name:tag name
                """
    return [node for node in elt.childNodes if node.nodeName == name]


def xml_find_node(elt, name):
    """xml_find_node

    :param elt:XML parent element
    :param name:tag name
        """
    nodes = xml_find_nodes(elt, name)
    return nodes[0] if len(nodes) == 1 else None


def fixed_writexml(self, writer, indent="", addindent="", newl=""):
    """fixed_writexml

    :param writer:XML node
    :param indent:current indentation
    :param addindent:indentation to add to higher levels
    :param newl:newline string
                """
    writer.write(indent + "<" + self.tagName)

    attrs = self._get_attributes()
    a_names = attrs.keys()
#     a_names.sort()

    for a_name in a_names:
        writer.write(" %s=\"" % a_name)
        minidom._write_data(writer, attrs[a_name].value)
        writer.write("\"")
    if self.childNodes:
        if len(self.childNodes) == 1 \
            and self.childNodes[0].nodeType \
                == minidom.Node.TEXT_NODE:
            writer.write(">")
            self.childNodes[0].writexml(writer, "", "", "")
            writer.write("</%s>%s" % (self.tagName, newl))
            return
        writer.write(">%s" % newl)
        for node in self.childNodes:
            fixed_writexml(
                    node, writer,
                    indent + addindent, addindent, newl)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))
