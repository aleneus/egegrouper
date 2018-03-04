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

""" Simple implementation of SME model. """

class Signal:
    """Signal."""

    def __init__(self):
        self._meta = {}
        self.x = []
    
    def set_dt(self, dt):
        self._meta['dt'] = dt
    def get_dt(self):
        return self._meta['dt']
    dt = property(get_dt, set_dt)    
    
class Measurement:
    """ Measurement which contains one or more signals. """
    def __init__(self):
        self._meta = {}
        self.ss = []

    def set_time(self, time):
        self._meta['time'] = time
    def get_time(self):
        return self._meta['time']
    time = property(get_time, set_time)    
    
class Examination:
    """ Examination, which contains one or more measurements. """
    def __init__(self):
        self._meta = {}
        self.ms = []

    def set_age(self, age):
        self._meta['age'] = age
    def get_age(self):
        return self._meta['age']
    age = property(get_age, set_age)

    def set_name(self, name):
        self._meta['name'] = name
    def get_name(self):
        return self._meta['name']
    name = property(get_name, set_name)
    
    def set_gender(self, gender):
        self._meta['gender'] = gender
    def get_gender(self):
        return self._meta['gender']
    gender = property(get_gender, set_gender)
    
    def set_diagnosis(self, diagnosis):
        self._meta['diagnosis'] = diagnosis
    def get_diagnosis(self):
        return self._meta['diagnosis']
    diagnosis = property(get_diagnosis, set_diagnosis)
    
def merge_exams(e1, e2):
    """Merge exams."""
    e = Examination()
    e = e1
    for m in e2.ms:
        e1.ms.append(m)
    return e
