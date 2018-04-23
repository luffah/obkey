# ObKey - Openbox Key Editor 
_(PyGObject version)_

![ObKey](wiki/screenshot_obkey.png)

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
[OpenBox](http://openbox.org/wiki/Main_Page) is really lightweight and stable.<br>
[OpenBox](http://openbox.org/wiki/Main_Page) is one of the most customizable Window Manager.<br>
[OpenBox](http://openbox.org/wiki/Main_Page) allows to precisely place windows and to easily switch without clicking a mouse.<br>
[OpenBox](http://openbox.org/wiki/Main_Page) configuration is written in XML, the configuration file is in `~/.config/openbox/rc.xml`.<br>
Some desktop environment use a custom configuration file...<br>
Hey, stop ! You don't need to edit directly the XML file, there's [ObConf](https://github.com/danakj/obconf) and [ObKey](#) !

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
md5sum obkey.deb | grep d4ab76711cbea8afcf88cb138e07a90d && echo OK

sudo apt install python-gi python-gettext
sudo dpkg -i obkey.deb
```

# About KeyBindings
For more informations : see [key bindings specification in OpenBox official site](http://openbox.org/wiki/Help:Bindings)

Alternatives :

* [obhotkey](https://sourceforge.net/projects/obhotkey/) _not updated since 2013..._ : allows to edit shortcut directly in a command line interface
* [lxhotkey](https://github.com/lxde/lxhotkey) : LXDE shortcut editor
