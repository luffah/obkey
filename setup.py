from distutils.core import setup
from glob import glob
import os

libdir = 'share/obkey/icons'
localedir = 'share/locale'

langs = [a[len("locale/"):] for a in glob('locale/*')]
locales = [(os.path.join(localedir, l, 'LC_MESSAGES'),
            [os.path.join('locale', l, 'LC_MESSAGES', 'obkey.mo')]) for l in langs]
install_requires=['gi', 'gettext']
setup(name='obkey',
      version='1.2pre',
      description='Openbox Key Editor',
      url='https://github.com/luffah/obkey',
      long_description="ObKey ease the keybindings configuration for Openbox.",
      author='luffah',
      author_email='luffah@runbox.com',
      scripts=['obkey'],
      py_modules=['obkey_classes'],
      data_files=[(libdir, ['icons/add_child.png', 'icons/add_sibling.png'])] + locales,
      keywords='openbox keybindings keys shortcuts',  # Optional
      project_urls={ 
         'Bug Reports': 'https://github.com/luffah/obkey/issues',
         'Source': 'https://github.com/luffah/obkey/',
        },
    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[  # Optional
          # How mature is this project? Common values are
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 4 - Beta',

          # Indicate who your project is intended for
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',

          # Pick your license as you wish
          'License :: OSI Approved :: MIT License',

          # Specify the Python versions you support here. In particular, ensure
          # that you indicate whether you support Python 2, Python 3 or both.
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          ],
)
