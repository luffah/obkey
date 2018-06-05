#!/usr/bin/python2
"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
"""
from os.path import join as path_join, dirname, isdir
import sys

# XXX: Sorry, for now this is it.
# If you know a better way to do this with setup.py:
# please mail me.

_ = None

class Resources(object):

    """Resources of the application"""

    def __init__(self, argv):
        """__init__

        :param argv:
        """
        global _
        if isdir('./resources/icons') and isdir('./resources/locale'):
            self.icons = './resources/icons'
            self.locale_dir = './resources/locale'
        else:
            config_prefix = dirname(dirname(argv[0]))
            self.icons = path_join(config_prefix, 'share/obkey/icons')
            self.locale_dir = path_join(config_prefix, 'share/locale')
        try:
            # from gettext import install as gettext_init
            import gettext
            gettext.bindtextdomain('obkey', self.locale_dir)
            gettext.textdomain('obkey')
            _ = gettext.gettext
            # gettext_init('obkey', self.locale_dir)
        except ImportError:
            print("Gettext is missing")
            def _(a):
                return a


    def getIcon(self, fname):
        """getIcon

        :param fname:
                """
        return path_join(self.icons, fname)


res = Resources(sys.argv)

