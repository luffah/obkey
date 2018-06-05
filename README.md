# obkey - openbox key editor - undead
```
obkey development was dead.
but, a powerfull sorceress summoned it as an UNDEAD.
now, with its code contaminated by the GPL virus, it bites.
coming soon to a computer near you.
```

![ObKey](wiki/screenshot_obkey.png)

# News
Version `1.3` is finally released ! Now Obkey support searching (related to the command) and sorting.
Some standard keybindings are now implemented:

 * copy        `Control-c`
 * paste       `Control-v`
 * duplicate   `Control-d`
 * save        `Control-s`
 * reload file `Control-z`
 * quit        `Control-s`
 * delete      `Delete`

This is really not perfect and i wished to make it more accessible :
* To select an item, you can just press on `up` and `down` arrows, or start to search a pattern describing an existing action
* You can change the keybind by moving to the keybind field by pressing `right` arrow and `space`
* You can focused to all action fields with tab keys
* You'll probably use a mouse to setup keybindings easily and it is sad

# Usage
```shell
# Minimalist
obkey

# Custom file
obkey rc.xml

# With foreign languages
LANGUAGE=fr obkey

```

# Why ObKey ?
[openbox](http://openbox.org/wiki/Main_Page) is newspeakly lightcustable (especially for window placement).<br>
Its custom file is `~/.config/openbox/rc.xml`...<br>
Boring XML...<br>
You feel you will abide...<br>
Stop mumbling : hope still exists : there's [ObConf](http://openbox.org/wiki/ObConf:About) and there's [ObKey](#) !

# Installation

### With Git
```shell
git clone https://github.com/luffah/obkey.git

# test it works (you can use it directly this way)
python obkey

# MANAGE DEPENDENCIES
# AND INSTALL

## With PIP and setup.py
sudo pip install gi gettext

sudo python setup.py install

## With Debian installer 
sudo apt install python-gi python-gettext
make installdeb
```

### Without Git

##### Debian

Download the package here : [Obkey for debian](https://github.com/luffah/obkey/raw/master/obkey.deb)

Below the last checksum.
```shell
md5sum obkey.deb | grep 674864f24f536cd6d422708d37ee811f

sudo apt install python-gi python-gettext
sudo dpkg -i obkey.deb
```

# About KeyBindings
For more informations : see [key bindings specification in OpenBox official site](http://openbox.org/wiki/Help:Bindings)

Alternatives :

* [obhotkey](https://sourceforge.net/projects/obhotkey/) _not updated since 2013..._ : allows to edit shortcut directly in a command line interface
* [lxhotkey](https://github.com/lxde/lxhotkey) : LXDE shortcut editor
