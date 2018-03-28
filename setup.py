#!/usr/bin/env python
"""
  Setup script
  Usage : python setup.py build
"""
from os.path import abspath, join, dirname
import io
from glob import glob
from distutils.core import setup
from obkey_parts import __version__, __description__, __long_description__
# Tests pass when  applications are stored in /usr/

NAME = 'obkey'
DESCRIPTION = __description__
URL = 'https://github.com/luffah/obkey'
LONG_DESCRIPTION = __long_description__
AUTHOR = 'luffah'
AUTHOR_EMAIL = 'luffah@runbox.com'
SCRIPTS = ['obkey']
# PY_MODULES=[a.replace('/','.').replace('.py','') for a in glob('obkey_parts/*.py')],
PACKAGES = ['obkey_parts']
PYTHON_REQUIRES = '>=2.7.0'
VERSION = __version__
LICENCES = 'MIT'
KEYWORDS = 'openbox keybindings keys shortcuts'

RES_ICONS = ('resources/icons', 'share/obkey/icons')
RES_LOCALES = ('resources/locale', 'share/locale')
RES_DESKTOP = ('misc', 'share/applications')
RES_APPDATA = ('misc', 'share/appdata')

LANGS = [a[len(RES_LOCALES[0] + '/'):] for a in glob(RES_LOCALES[0] + '/*')]

INSTALL_REQUIRES = ['gi', 'gettext']

DATA_FILES = [
    (RES_ICONS[1],
     [RES_ICONS[0] + '/add_child.png', RES_ICONS[0] + '/add_sibling.png']),
    (RES_DESKTOP[1],
     [RES_DESKTOP[0] + '/obkey.desktop'],),
    (RES_APPDATA[1],
     [RES_APPDATA[0] + '/obkey.appdata.xml'],)
] + [
    (join(RES_LOCALES[1], l, 'LC_MESSAGES'),
     [join(RES_LOCALES[0], l, 'LC_MESSAGES', 'obkey.mo')]) for l in LANGS
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    scripts=SCRIPTS,
    install_requires=INSTALL_REQUIRES,
    # py_modules=PY_MDULES,
    packages=PACKAGES,
    # packages=find_packages(),
    data_files=DATA_FILES,
    license=LICENCES,
    keywords=KEYWORDS,
    platform='Linux',
    project_urls={
        'Bug Reports': 'https://github.com/luffah/obkey/issues',
        'Source': 'https://github.com/luffah/obkey/',
        },
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Desktop Environment :: Window Managers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: POSIX :: Linux',
        # 'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ]
    )
