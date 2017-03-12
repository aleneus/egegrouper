#! /usr/bin/env python3
#

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
sys.path.insert(0, os.path.abspath('../'))

from egegmvc.sqlite3_model import Model

class TestSqliteModel(unittest.TestCase):
    
    def test_create_storage(self):
        """Test the fact of storage creation."""
        m = Model()
        file_name = './file.sme.sqlite'
        if os.path.isfile(file_name):
            os.remove(file_name)
        m.create_storage(file_name)
        exists = os.path.isfile(file_name)
        if os.path.isfile(file_name):
            os.remove(file_name)
        self.assertEqual(exists, True)

    def test_create_storage_if_exists(self):
        """If file file_name exists it should be correctly replaced by new storage."""
        m = Model()
        file_name = './file.sme.sqlite'
        if os.path.isfile(file_name):
            os.remove(file_name)
        m.create_storage(file_name)
        result = m.create_storage(file_name)
        if os.path.isfile(file_name):
            os.remove(file_name)
        self.assertEqual(result, True)

    def test_create_storage_with_bad_file_name(self):
        """If the storage has some bad file_name, the model should return False."""
        m = Model()
        result = m.create_storage('..')
        self.assertEqual(result, False)

    def test_get_examination(self):
        """Get examination by ID from data base."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        e = m.exam(1)
        self.assertNotEqual(e, None)

    def test_get_no_existing_examination(self):
        """Try to get examination from data base by no existing exam_id."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        e = m.exam(1000)
        self.assertEqual(e, None)


unittest.main()
