from distutils.core import setup
from glob import glob
import os

# assuming applications are stored in /usr/
libdir = 'share/obkey/icons'
localedir = 'share/locale'
desktopdir = 'share/applications'

res_icons = 'resources/icons'
res_locales = 'resources/locale'
res_desktop = 'misc'

langs = [a[len(res_locales + '/'):] for a in glob(res_locales + '/*')]
install_requires = ['gi', 'gettext']
setup(name='obkey',
      version='1.2',
      description='Openbox Key Editor',
      url='https://github.com/luffah/obkey',
      long_description="ObKey ease the keybindings configuration for Openbox.",
      author='luffah',
      author_email='luffah@runbox.com',
      scripts=['obkey'],
      py_modules=['obkey_classes'],
      data_files=[(
          libdir,
          [res_icons + '/add_child.png', res_icons + '/add_sibling.png']
      ), (
          desktopdir,
          [res_desktop + '/obkey.desktop'],

      )] + [(
            os.path.join(localedir, l, 'LC_MESSAGES'),
            [os.path.join(res_locales, l, 'LC_MESSAGES', 'obkey.mo')]
            ) for l in langs],
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
