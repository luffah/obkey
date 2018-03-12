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
from obkey_parts.Gui import Gtk
# =========================================================
# Key utils
# =========================================================

REPLACE_TABLE_OPENBOX2GTK = {
    "mod1": "<Mod1>", "mod2": "<Mod2>",
    "mod3": "<Mod3>", "mod4": "<Mod4>", "mod5": "<Mod5>",
    "control": "<Ctrl>", "c": "<Ctrl>",
    "alt": "<Alt>", "a": "<Alt>",
    "meta": "<Meta>", "m": "<Meta>",
    "super": "<Super>", "w": "<Super>",
    "shift": "<Shift>", "s": "<Shift>",
    "hyper": "<Hyper>", "h": "<Hyper>"
}

REPLACE_TABLE_GTK2OPENBOX = {
    "Mod1": "Mod1", "Mod2": "Mod2",
    "Mod3": "Mod3", "Mod4": "Mod4", "Mod5": "Mod5",
    "Control": "C", "Primary": "C",
    "Alt": "A",
    "Meta": "M",
    "Super": "W",
    "Shift": "S",
    "Hyper": "H"
}


def key_openbox2gtk(obstr):
    """key_openbox2gtk

    :param obstr:
                """
    if obstr is not None:
        toks = obstr.split("-")
    try:
        toksgdk = [REPLACE_TABLE_OPENBOX2GTK[mod.lower()] for mod in toks[:-1]]
    except BufferError:
        return (0, 0)
    toksgdk.append(toks[-1])
    return Gtk.accelerator_parse("".join(toksgdk))


def key_gtk2openbox(key, mods):
    """key_gtk2openbox

    :param key:
    :param mods:
    """
    result = ""
    if mods:
        modtable = Gtk.accelerator_name(0, mods)
        modtable = [
                REPLACE_TABLE_GTK2OPENBOX[i]
                for i in modtable[1:-1].split('><')
                ]
        result = '-'.join(modtable)
    if key:
        keychar = Gtk.accelerator_name(key, 0)
        if result != "":
            result += '-'
        result += keychar
    return result
