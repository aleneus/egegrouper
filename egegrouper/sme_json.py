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

"""Mapping examinations to and from JSON files."""

import json
import numpy as np
import os, shutil
from collections import OrderedDict

from . import sme

def get_exam(file_name):
    """Get examination object from JSON file.

    Parameters
    ----------
    file_name : str
        Name of JSON file.
    
    Return
    ------
    : sme.Examination
        Examination instance.

    """
    abs_file_name = os.path.expanduser(file_name)
    abs_data_folder_name = "{}.data".format(abs_file_name)
    e = sme.Examination()
    with open(abs_file_name, 'r') as f:
        data = json.load(f)
    e.name = data['name']
    e.age = data['age']
    e.gender = data['gender']
    e.diagnosis = data['diagnosis']
    e.ms = []
    for m_data in data['measurements']:
        m = sme.Measurement()
        m.time = m_data['time']
        m.ss = []
        for s_data in m_data['signals']:
            s = sme.Signal()
            s.dt = s_data['dt']
            s.x = np.loadtxt(
                os.path.join(
                    abs_data_folder_name,
                    s_data['file']
                )
            )
            m.ss.append(s)
        e.ms.append(m)
    return e

def put_exam(e, file_name):
    """Put examination to JSON file.

    Parameters
    ----------
    e : sme.Examination
        Examination instance.
    file_name : str
        File name.
    
    """
    abs_file_name = os.path.expanduser(file_name)
    abs_data_folder_name = "{}.data".format(abs_file_name)
    if os.path.isfile(abs_file_name):
        os.remove(abs_file_name)
    if os.path.isdir(abs_data_folder_name):
        shutil.rmtree(abs_data_folder_name)
    os.makedirs(abs_data_folder_name)
    e_dict = OrderedDict()
    e_dict['name'] = e.name
    e_dict['diagnosis'] = e.diagnosis
    e_dict['age'] = e.age
    e_dict['gender'] = e.gender
    e_dict['measurements'] = []
    for (m, mn) in zip(e.ms, range(1, len(e.ms)+1)):
        m_dict = OrderedDict()
        m_dict['time'] = m.time
        m_dict['signals'] = []
        for (s, sn) in zip(m.ss, range(1, len(m.ss)+1)):
            s_dict = OrderedDict()
            s_dict['dt'] = s.dt
            signal_file_name = 'signal-{}{}.txt'.format(mn, sn)
            s_dict['file'] = signal_file_name
            np.savetxt(
                os.path.join(
                    abs_data_folder_name,
                    signal_file_name
                ),
                s.x,
                fmt='%f'
            )
            m_dict['signals'].append(s_dict)
        e_dict['measurements'].append(m_dict)
    s = json.dumps(e_dict, ensure_ascii=False, indent='    ')
    with open(abs_file_name, 'w') as f:
        f.write(s)
