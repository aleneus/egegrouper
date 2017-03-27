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
from egegrouper.sme_json import *

from preparation import *

class TestSmeJsonFolders(unittest.TestCase):
    
    def test_syntax(self):
        """Syntax."""
        pass

    def test_put_exam_creates_correct_json_file(self):
        e = create_test_exam()
        file_name = "example.json"
        folder_name = "{}.data".format(file_name)
        remove_file(file_name)
        remove_folder(folder_name)
        put_exam(e, file_name)
        result = os.path.isfile(file_name)
        remove_file(file_name)
        remove_folder(folder_name)
        self.assertTrue(result)

    def test_put_exam_creates_correct_data_folder(self):
        e = create_test_exam()
        file_name = "example.json"
        folder_name = "{}.data".format(file_name)
        remove_file(file_name)
        remove_folder(folder_name)
        put_exam(e, file_name)
        result = os.path.isdir(folder_name)
        remove_file(file_name)
        remove_folder(folder_name)
        self.assertTrue(result)

    def test_put_exam_creates_signal_file_in_data_folder(self):
        e = create_test_exam()
        file_name = "example.json"
        folder_name = "{}.data".format(file_name)
        remove_file(file_name)
        remove_folder(folder_name)
        put_exam(e, file_name)
        result = os.path.isfile(os.path.join(
            folder_name,
            "signal-11.txt"
        ))
        remove_file(file_name)
        remove_folder(folder_name)
        self.assertTrue(result)

    def test_put_exam_creates_not_empty_signal_file_in_data_folder(self):
        e = create_test_exam()
        file_name = "example.json"
        folder_name = "{}.data".format(file_name)
        remove_file(file_name)
        remove_folder(folder_name)
        put_exam(e, file_name)
        result = os.path.getsize(
            os.path.join(
                folder_name,
                "signal-11.txt"
            )   
        )
        remove_file(file_name)
        remove_folder(folder_name)
        self.assertTrue(result > 0)

    def test_put_exam_creates_correct_json_file_using_home_dir(self):
        e = create_test_exam()
        file_name = "~/example.json"
        folder_name = "{}.data".format(file_name)
        print(os.path.expanduser(folder_name))
        remove_file(os.path.expanduser(file_name))
        remove_folder(os.path.expanduser(folder_name))
        put_exam(e, file_name)
        result = os.path.isfile(os.path.expanduser(file_name))
        remove_file(os.path.expanduser(file_name))
        remove_folder(os.path.expanduser(folder_name))
        self.assertTrue(result)

    def test_get_json_gives_not_empty_object(self):
        file_name = "test.json"
        e = get_exam(file_name)
        self.assertFalse(e == None)

    def test_get_json_gives_correct_measurements_number(self):
        file_name = "test.json"
        e = get_exam(file_name)
        self.assertEqual(len(e.ms), 2)

    def test_get_json_gives_not_empty_signal(self):
        file_name = "test.json"
        e = get_exam(file_name)
        self.assertTrue(len(e.ms[0].ss[0].x) > 0)

    def test_get_json_gives_corrent_name_of_patient(self):
        file_name = "test.json"
        e = get_exam(file_name)
        self.assertEqual(e.name, "Anonym")
