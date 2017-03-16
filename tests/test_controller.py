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

from .context import egegrouper
from egegrouper.controller import Controller

import unittest
import os

class ModelStub:
    def create_storage(self, name):
        if name=='bad_name':
            raise Exception
        else:
            return True

    def storage_info(self):
        return None, None

    def exam(self, exam_id):
        if exam_id == 'raise_excetion':
            raise AttributeError('Test')
        if exam_id == '1':
            return 'examination data'
        if exam_id == '1000':
            return None

class ViewStub:
    def show_data(*args):
        pass

class TestController(unittest.TestCase):

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_syntax(self):
        pass
    
    def test_create_storage(self):
        c = Controller(ModelStub())
        result = c.create_storage('bad_name')
        self.assertFalse(result)

    def test_exam_with_existing_id(self):
        c = Controller(ModelStub())
        c.set_view_exam(ViewStub())
        result = c.exam('1')
        self.assertTrue(result)
        
    def test_exam_with_no_existing_id(self):
        c = Controller(ModelStub())
        result = c.exam('1000')
        self.assertTrue(result)
        
    def test_exam_if_model_raising_exception(self):
        c = Controller(ModelStub())
        result = c.exam('raise_excetion')
        self.assertFalse(result)
        
    def test_plot_exam_with_existing_id(self):
        c = Controller(ModelStub())
        c.set_view_exam_plot(ViewStub())
        result = c.plot_exam('1')
        self.assertTrue(result)
        
    def test_plot_exam_with_no_existing_id(self):
        c = Controller(ModelStub())
        result = c.plot_exam('1000')
        self.assertTrue(result)
        
    def test_plot_exam_if_model_raising_exception(self):
        c = Controller(ModelStub())
        result = c.plot_exam('raise_excetion')
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
