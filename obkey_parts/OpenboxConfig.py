"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
"""
from os import system
from obkey_parts.XmlUtils import (
        minidom, xml_find_node, fixed_writexml
)


class OpenboxConfig:

    """OpenboxConfig"""

    def __init__(self):
        """__init__"""
        self.dom = None
        self.keyboard = None
        self.path = None

    def load(self, path=None):
        """load

        :param path:
        """
        if path:
            self.path = path

        # load config DOM
        self.dom = minidom.parse(self.path)

        # try load keyboard DOM
        self.keyboard_node = xml_find_node(
                self.dom.documentElement,
                "keyboard"
        )

    def save(self, keyboard_node):
        """save

        :param keyboard_node:
        """
        if self.path is None:
            return

        newdom = xml_find_node(
                fixed_writexml(keyboard_node, "  ", "  ", "\n"),
                "keyboard"
                )
        keyboard = xml_find_node(
                self.dom.documentElement,
                "keyboard"
                )
        self.dom.documentElement.replaceChild(newdom, keyboard)
        with open(self.path, "w") as f:
            xmlform = self.dom.documentElement
            f.write(xmlform.toxml("utf8"))
        self.reconfigure_openbox()

    def reconfigure_openbox(self):
        """reconfigure_openbox"""
        system("openbox --reconfigure")
