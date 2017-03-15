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

"""Very simple implementation of SME model."""

class Signal:
    """Signal."""
    
    dt = None
    """Sample step."""
    x = []
    """Samples values."""
    
class Measurement:
    """Measurement.

    Measurement contains one or more signals. 
    
    """

    time = None
    """Measurement start time."""
    ss = []
    """Signals."""
    
class Examination:
    """Examination.

    Examination contains one or more measurements.

    """
    
    name = None
    """Name of patient."""
    
    age = None
    """Age of patient."""
    
    gender = None
    """Gender of patient."""
    
    diagnosis = None
    """Diagnosis."""
    
    ms = []
    """Measurements."""
    
def merge_exams(e1, e2):
    """Merge exams."""
    e = Examination()
    e = e1
    for m in e2.ms:
        e1.ms.append(m)
    return e
