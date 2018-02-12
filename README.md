# obkey
ObKey - Openbox Key Editor (PyGObject version)

![ObKey](wiki/screenshot_obkey.png)

# Installation

```shell
git clone https://github.com/luffah/obkey.git

# test it works (you can use it directly this way)
python obkey

# INSTALLATION
sudo python setup.py

# Finally run obkey
obkey

# to try other languages
LANGUAGE=fr obkey

```

# Dependencies

### with PIP

```shell
sudo pip install gi gettext
```
### with APT

```shell
sudo apt install python-gi python-gettext
```

# About me
After tried almost every window managers,
and having recently left my 'awesomewm' configuration behind a sharp #.

I use OpenBox on my low ressource machine, because it allows to change
windows with direction (north, east, south, west) which is really intuitive way to switch focus.

Another easy to use capability in OpenBox, is the Emacs style multi-levels shorcut.

But, it is really boring to edit OpenBox XML rc file.
After searching in some forums, i found ObKey, which is usefull, but not perfectly usable.
So i forked the project.

# Bugs/Enhancement (Reasons of this fork)
- you can set keybings, save them, close, and re-open the tool and see that it has disappeared
- you cannot organize your keybinding collection with drag and drop

- if a problem occur about internationnalization (gettext), you may need to do next procedure to solve it :

```shell
# check the lang is well detected in installation pack
./obkey ~/.config/openbox TESTING

# if gettext is not found, you shall have a message saying that gettext is missing

# take the name of the translation file
tMSGFILE=LC_MESSAGES/obkey.mo

# find the translation directory
tPYTHONPATH=`python -c "import sys; print '\n'.join(sys.path)" | grep 'lib/python'`
tPYLANGPATH=`find $tPYTHONPATH -name 'gettext.py' | xargs grep 'mofile_lp =' | sed 's/.*join("\(.*\)".*$/\1/'`

if [ -d $tPYLANGPATH ]
then
  ls -1 locale/ | xargs -I{} sudo cp locale/{}/$tMSGFILE $tPYLANGPATH/{}/$tMSGFILE
fi
```
# Changes between obkey 1.1 and obkey 1.2 
- sorted actions in edition pane
- direct preview of relations between actions and keybind

TODO -> button to sort the keybind / drag and drop / alerting users on failure


# About

This fork aims to continue the project since bugs and enhancement stills needed.

Another wish for the future could be the integration :
 - _either_ integration this tool for other window manager (e.g. xmonad)
 - _or_ integration in a setting manager for OpenBox

# About KeyBindings
Key bindings in OpenBox official site :

http://openbox.org/wiki/Help:Bindings

If you want to edit shortcut directly in  command line interface,
see the next project (not updated since 2013...): https://sourceforge.net/projects/obhotkey/

The more serious alternative to obkey is probably lxhotkey : https://github.com/lxde/lxhotkey
