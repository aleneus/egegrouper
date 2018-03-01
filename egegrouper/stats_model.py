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
