"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from setuptools import setup

setup(
    name='EGEGrouper',
    version='0.1',
    description='Tool for grouping EGEG examinations',
    author='Aleksandr Popov',
    author_email='aleneus@gmail.com',
    packages=['egegrouper'],
    #scripts=['tkgrouper.py', 'igrouper.py'],
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
)
