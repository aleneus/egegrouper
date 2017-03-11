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

from egegmvc.controller import Controller

class ModelStub:
    def create_storage(self, name):
        if name=='bad_name':
            return False
        else:
            return True

    def storage_info(self):
        return None, None

class TestController(unittest.TestCase):
    
    def test_create_storage(self):
        """Test create storage."""
        c = Controller(ModelStub())
        result = c.create_storage('bad_name')
        self.assertEqual(result, False)

unittest.main()
