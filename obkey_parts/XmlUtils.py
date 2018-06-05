"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
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


def fixed_writexml(self, indent="", addindent="", newl="", writer=None):
    """fixed_writexml

    :param self:XML node
    :param indent:current indentation
    :param addindent:indentation to add to higher levels
    :param newl:newline string
    """
    # the root of recursion tree
    proot = False
    # it's all hack, waste of resources etc, but does pretty good result
    if not writer:
        from StringIO import StringIO
        writer = StringIO()
        proot = True

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
                    node,
                    indent + addindent, addindent, newl, writer)
        writer.write("%s</%s>%s" % (indent, self.tagName, newl))
    else:
        writer.write("/>%s" % (newl))

    return parseString(writer.getvalue()) if proot else None
