# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017 Aleksandr Popov

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

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="EGEGrouper",
    version="0.1.1",
    description="Tool for grouping EGEG examinations",
    author="Aleksandr Popov",
    author_email="aleneus@gmail.com",
    license = "GPLv3",
    keywords = "electrophysiology electrogastrography electrogastroenterography biosignal storage dataset",
    url = "https://bitbucket.org/aleneus/egegrouper",
    long_description=read('README'),
    packages=['egegrouper'],
    install_requires = [
        'numpy',
        'matplotlib',
        'tabulate',
        'nose',
        'pyreadline;platform_system=="Windows"',
    ],
    entry_points={
        'console_scripts': [
            'igrouper = egegrouper.igrouper:main'
        ],
        'gui_scripts': [
            'tkgrouper = egegrouper.tkgrouper:main'
        ]
    },
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
    ],
)
