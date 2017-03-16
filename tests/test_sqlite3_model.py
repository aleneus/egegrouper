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
import shutil
import sqlite3

from .context import egegrouper
from egegrouper import *
from egegrouper.sqlite3_model import Model
from egegrouper import sme

from preparation import *

class TestSqliteModel(unittest.TestCase):
    
    def test_syntax(self):
        """Syntax."""
        pass

    def test_create_storage(self):
        """Test the fact of storage creation."""
        m = Model()
        file_name = './file.sme.sqlite'
        remove_file(file_name)
        m.create_storage(file_name)
        exists = os.path.isfile(file_name)
        remove_file(file_name)
        self.assertEqual(exists, True)

    def test_create_storage_if_exists(self):
        """If file file_name exists it should be correctly replaced by new storage."""
        m = Model()
        file_name = './copy-test.sme.sqlite'
        shutil.copy2('./test.sme.sqlite', file_name)
        m.create_storage(file_name)
        m.close_storage()
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
        c.execute("select count(*) from examination")
        n = c.fetchone()[0]
        conn.close()
        remove_file(file_name)
        self.assertEqual(n, 0)

    # get examination

    def test_get_examination_naive(self):
        """Get examination record by ID from data base."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        e = m.exam(1)
        self.assertNotEqual(e, None)

    def test_get_examination(self):
        """Get examination by ID from data base."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        e = m.exam(1)
        self.assertEqual(len(e.ms), 2)

    def test_get_no_existing_examination(self):
        """Try to get examination from data base by no existing exam_id."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        e = m.exam(1000)
        self.assertEqual(e, None)

    # insert examination

    def test_insert_examination(self):
        """Number of examination must be increase after insert examination."""
        m = Model()
        file_name = './copy-test.sme.sqlite'
        shutil.copy2('./test.sme.sqlite', file_name)
        def get_len():
            conn = sqlite3.connect(file_name)
            c = conn.cursor()
            c.execute("select count(*) from examination")
            return c.fetchone()[0]
            conn.close()
        len_before = get_len()
        m.open_storage(file_name)
        m.insert_exam(create_test_exam())
        m.close_storage()
        len_after = get_len()
        remove_file(file_name)
        self.assertTrue(len_after > len_before)

    def test_insert_examination_if_storage_was_not_open(self):
        """Insert examination method must return False if storage was not open."""
        m = Model()
        file_name = './copy-test.sme.sqlite'
        shutil.copy2('./test.sme.sqlite', file_name)
        try:
            m.insert_exam(create_test_exam())
            result = True
        except AttributeError:
            result = False
        finally:
            self.assertFalse(result)

    def test_insert_examination_to_new_storage(self):
        """Number of examination must be 1 after insertion examination to new empty storage."""
        m = Model()
        file_name = './copy-test.sme.sqlite'
        m.create_storage(file_name)
        m.insert_exam(create_test_exam())
        m.close_storage()
        conn = sqlite3.connect(file_name)
        c = conn.cursor()
        c.execute("select count(*) from examination")
        n = c.fetchone()[0]
        conn.close()
        remove_file(file_name)
        self.assertEqual(n, 1)

    # storage info

    def test_storage_info(self):
        m = Model()
        m.open_storage('./test.sme.sqlite')
        data, headers = m.storage_info()
        self.assertEqual(len(data) > 0, True)
        self.assertEqual(len(headers) > 0, True)

    def test_storage_info_if_storage_not_opened(self):
        m = Model()
        try:
            m.storage_info()
            result = True
        except AttributeError:
            result = False
        finally:
            self.assertFalse(result)

    # group info

    def test_group_info_by_existing_not_zero_id(self):
        m = Model()
        m.open_storage('./test.sme.sqlite')
        data, headers = m.group_info(1)
        self.assertNotEqual(data, None)
        self.assertNotEqual(headers, None)

    def test_get_ungrouped(self):
        """Storage info result must be not empty if storage was opened."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        data, headers = m.group_info('0')
        self.assertNotEqual(data, None)
        self.assertNotEqual(headers, None)

    def test_group_info_if_group_does_not_exist(self):
        """Storage info result must be not empty if storage was opened."""
        m = Model()
        m.open_storage('./test.sme.sqlite')
        data, headers = m.group_info(1000)
        self.assertEqual(data, None)
        self.assertEqual(headers, None)

if __name__ == '__main__':
    unittest.main()
