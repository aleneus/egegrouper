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

class StatsModel:
    """ The model class providing some descriptive statistics of
    groups. """
    def __init__(self, data_provider=None):
        """ Initialization. """
        # TODO: doc details
        self.set_data_provider(data_provider)
    
    def set_data_provider(self, data_provider):
        """ Set the model providing the access to data. """
        # TODO: doc details
        self.data_provider = data_provider
        
    def gender_balance(self, group_id):
        """ Return the dictionary with number of examinations for
        males and females. """
        # TODO: doc details
        es = self.data_provider.exams(group_id)
        res = {}
        for e in es:
            key = e.gender
            if key not in res:
                res[key] = 1
            else:
                res[key] += 1
        return res

    def aver_age(self, group_id):
        """ Return the average age of patients in the group. """
        # TODO: doc details
        es = self.data_provider.exams(group_id)
        ages = [e.age for e in es]
        res = np.average(ages)
        return res
