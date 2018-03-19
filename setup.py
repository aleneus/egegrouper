# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
import os

import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

from egegrouper.glob import *

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

name="EGEGrouper"
description="Tool for grouping EGEG examinations"
author="Aleksandr Popov"
author_email="aleneus@gmail.com"
license = "GPLv3"
keywords = "electrophysiology electrogastrography electrogastroenterography biosignal storage dataset"
url = "https://bitbucket.org/aleneus/egegrouper"
packages=['egegrouper']

package_data={
    'egegrouper': [
        'icons/*.gif',
    ],
}

install_requires = [
    'numpy',
    'matplotlib',
    'tabulate',
    'nose',
    'pyreadline;platform_system=="Windows"',
]

entry_points={
    'console_scripts': [
        'igrouper = egegrouper.igrouper:main'
    ],
    'gui_scripts': [
        'tkgrouper = egegrouper.tkgrouper:main'
    ]
}

classifiers=[
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: X11 Applications",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python :: 3",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

def linux_setup():
    setup(
        name=name,
        version=VERSION,
        description=description,
        author=author,
        author_email=author_email,
        license = license,
        keywords = keywords,
        url = url,
        long_description=read('README'),
        packages=packages,
        package_data=package_data,
        install_requires = install_requires,
        entry_points=entry_points,
        classifiers=classifiers,
    )

windows_options = {'build_exe': 
    {
        'includes': ['numpy.core._methods', 'numpy.lib.format', 'sqlite3'],
        'packages': ['pkg_resources._vendor', 'tkinter', 'matplotlib'],
        'include_files':[
            (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
            (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll')),
            (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'sqlite3.dll'), os.path.join('lib', 'sqlite3.dll'))
        ],
        'excludes': ['PyQt5'],
    }
}

def windows_build():
    setup(
        name=name,
        version=VERSION,
        description=description,
        author=author,
        author_email=author_email,
        keywords = keywords,
        long_description=read('README'),
        packages=packages,
        package_data=package_data,
        classifiers=classifiers,
        options = windows_options,
        executables = [
            # Executable("tkgrouper", base = "Win32GUI"),
            Executable("tkgrouper"),
        ],
    )

linux_setup()
#from cx_Freeze import setup, Executable
#windows_build()
