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

""" This module implements the model for doing some descriptive
statistics. """

import numpy as np
from collections import OrderedDict

class StatsModel:
    """ The model class providing some descriptive statistics of
    groups. """
    def __init__(self, data_provider=None):
        """ Initialization. """
        # TODO: doc details
        self.data_provider = data_provider
        self.age_bounds = []
    
    def number_by_meta(self, key, exams=None):
        """ Group examinations by the meta data key and return the
        number of examinations in each group. """
        if exams is None:
            exams = self.data_provider.exams(group_id)
        res = OrderedDict()
        for e in exams:
            value = e._meta[key]
            if value not in res:
                res[value] = 1
            else:
                res[value] += 1
        return res

    def set_age_groups(self, bounds: list):
        """ Set bounds of age groups. """
        self.age_bounds = bounds

    def age_stats(self, group_id=None, exams=None):
        """ Return the average age of patients in the group. """
        if exams is None:
            exams = self.data_provider.exams(group_id)

        def get_key(b):
            return '{}-{}'.format(b[0], b[1])
        
        ages = [e.age for e in exams]
        res = OrderedDict()
        for b in self.age_bounds:
            res[get_key(b)] = 0
        for age in ages:
            for b in self.age_bounds:
                if b[0] <= age <= b[1]:
                    res[get_key(b)] += 1
        return res

    def stats(self, key, group_id):
        """ Return statistics for group by gender, diagnosis or age group. """
        es = self.data_provider.exams(group_id, meta_only=True)

        res = OrderedDict()
        if key in ['gender', 'diagnosis']:
            res = self.number_by_meta(key, exams=es)
        elif key == 'age':
            self.set_age_groups([(0,19), (20,29), (30,39), (40,49),
                                 (50,59), (60,69), (70,79), (80,100)])
            res = self.age_stats(exams=es)
            
        return res
