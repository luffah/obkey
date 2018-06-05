"""
  Obkey package informations.

  This file is a part of Openbox Key Editor
  Code under GPL (originally MIT) from version 1.3 - 2018.
  See Licenses information in ../obkey .
"""
MAJOR = 1
MINOR = 3
PATCH = 1

__version__ = "{0}.{1}.{2}".format(MAJOR, MINOR, PATCH)

__description__ = 'Openbox Key Editor'
__long_description__ = """
A keybinding editor for OpenBox, it includes launchers and window management keys.

It allows to:
    * can check almost all keybinds in one second.
    * add new keybinds, the default key associated will be 'a' and no action will be associated;
    * add new child keybinds;
    * setup existing keybinds :
        * add/remove/sort/setup actions in the actions list;
        * change the keybind by clicking on the item in the list;
    * duplicate existing keybinds;
    * remove a keybind.

The current drawbacks :
    * XML inculsion is not managed. If you want to edit many files, then you shall open them with `obkey <config file>.xml`;
    * `if` conditionnal tag is not supported (but did you knew it exists).

"""
