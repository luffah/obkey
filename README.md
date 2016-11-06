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

########################################
## To solve INTERNATIONALIZATION PROBLEM
#  a workaround has been added in obkey_classes.py to find automaticaly the config_prefix
#  if this problem persist read this part 

## Solve the INTERNATIONALIZATION PROBLEM
# obkey have translation, but currently there's a bug on installation
#  due to an inconsistency between the lib 'obkey_classes.py' (line 48) and the installation made by 'setup.py'
# you may need to do next procedure to solve it

# take the name of the translation file
tMSGFILE=LC_MESSAGES/obkey.mo

# find the translation directory
# the default directory for python gettext shall be something like /usr/share/locale-langpack

tPYTHONPATH=`python -c "import sys; print '\n'.join(sys.path)" | grep 'lib/python2.7$'`
tPYLANGPATH=`find $tPYTHONPATH -name 'gettext.py' | xargs grep 'mofile_lp =' | sed 's/.*join("\(.*\)".*$/\1/'`

echo $tPYLANGPATH

if [ -d $tPYLANGPATH ]
then
  ls -1 locale/ | xargs -I{} sudo cp locale/{}/$tMSGFILE $tPYLANGPATH/{}/$tMSGFILE
fi

#############################

# Finally run obkey
obkey

# to try other languages
LANGUAGE=fr obkey

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
see the next project :

https://sourceforge.net/projects/obhotkey/
