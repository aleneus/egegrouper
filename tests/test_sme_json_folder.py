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

import unittest
import os
import sys
import shutil
import sqlite3

from .context import egegrouper
from egegrouper import sme
from egegrouper.sme_json_folders import *

from preparation import *

class TestSmeJsonFolders(unittest.TestCase):
    
    def test_syntax(self):
        """Syntax."""
        pass

    def test_put_exam_to_folder_creates_info(self):
        e = create_test_exam()
        folder_name = './exported_jfolder'
        remove_folder(folder_name)
        put_exam_to_folder(e, folder_name)
        result = os.path.isfile(os.path.join(folder_name, 'info.json'))
        remove_folder(folder_name)
        self.assertTrue(result)

    def test_put_exam_to_folder_creates_signal(self):
        e = create_test_exam()
        folder_name = './exported_jfolder'
        remove_folder(folder_name)
        put_exam_to_folder(e, folder_name)
        result = os.path.isfile(os.path.join(folder_name, 'signal-11.txt'))
        remove_folder(folder_name)
        self.assertTrue(result)
