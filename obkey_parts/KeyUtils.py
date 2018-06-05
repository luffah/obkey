"""
  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
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
