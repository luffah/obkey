#!/usr/bin/python2
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
import __builtin__
from os.path import join as path_join, dirname, isdir
import sys

# XXX: Sorry, for now this is it.
# If you know a better way to do this with setup.py:
# please mail me.


class Resources(object):

    """Resources of the application"""

    def __init__(self, argv):
        """__init__

        :param argv:
                """
        if isdir('./resources/icons') and isdir('./resources/locale'):
            self.icons = './resources/icons'
            self.locale_dir = './resources/locale'
        else:
            config_prefix = dirname(dirname(argv[0]))
            self.icons = path_join(config_prefix, 'share/obkey/icons')
            self.locale_dir = path_join(config_prefix, 'share/locale')
        try:
            from gettext import install as gettext_init
            gettext_init('obkey', self.locale_dir)
        except ImportError:
            print "Gettext is missing"

            def _(a):
                return a

    def getIcon(self, fname):
        """getIcon

        :param fname:
                """
        return path_join(self.icons, fname)


res = Resources(sys.argv)

# trick for syntax checkers
_ = __builtin__.__dict__['_']
