# obkey - openbox key editor - undead

| Year | Repo | Obkey Status  | Is maintained | 
| :-----   | :-----   | :-----   | :-----   |
| < 2018 | https://github.com/nsf/obkey | ? |  no |
| 2018-2019 | https://github.com/luffah/obkey | Somehow stable | no |
| 2022 |  https://github.com/MX-Linux/obkey | Being rewritten in Python3 by jerry3904 | wip |


```
ObKey development was dead.
it was reborn. and is sleeping again.

Actually, i no more use OpenBox since 2019.

If you use OpenBox and want to ensure ObKey still working well, feel free to grab the project
and notify in Issues you are improving it (there may have technical question you can ask).
```


![ObKey](wiki/screenshot_obkey.png)

# Changelog
2019 - Version `1.3` : Obkey support searching (related to the command) and sorting.
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
[openbox](http://openbox.org/wiki/Main_Page) is a very customizable Window Manager.<br>
Its custom file is `~/.config/openbox/rc.xml`...<br>
For configuring it from GUI, there's [ObConf](http://openbox.org/wiki/ObConf:About) and there's [ObKey](#) !

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
md5sum obkey.deb | grep e17d96e787b7cdc8363ec04ee5788d2e

# Old Checksums
# v1.3.1 (2018-06-05) 674864f24f536cd6d422708d37ee811f
# v1.3.2 (2019-05-03) e17d96e787b7cdc8363ec04ee5788d2e

sudo apt install python-gi python-gettext
sudo dpkg -i obkey.deb
```

# About KeyBindings
For more informations : see [key bindings specification in OpenBox official site](http://openbox.org/wiki/Help:Bindings)

Alternatives :

* [obhotkey](https://sourceforge.net/projects/obhotkey/) _not updated since 2013..._ : allows to edit shortcut directly in a command line interface
* [lxhotkey](https://github.com/lxde/lxhotkey) : LXDE shortcut editor
