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

"""Mapping examinations to and from JSON folders.

JSON folder is the folder that consists file info.json and signals in simple text format."""

import json
import numpy as np
import os
from collections import OrderedDict

from . import sme

def get_exam_from_folder(folder_name):
    """Get examination object from folder with file info.json.

    Parameters
    ----------
    folder_name : str
        Name of JSON folder.
    
    Return
    ------
    : sme.Examination
        Examination instance.

    """
    e = sme.Examination()
    with open('{}/info.json'.format(folder_name), 'r') as f:
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
            s.x = np.loadtxt('{}/{}'.format(folder_name, s_data['file']))
            m.ss.append(s)
        e.ms.append(m)
    return e

def put_exam_to_folder(e, folder_name):
    """Put examination to folder. Return True if sucsess, False overwise.

    Create info.json and text files with samples.

    Parameters
    ----------
    e : sme.Examination
        Examination instance.
    folder_name : str
        Folder name.
    
    """
    abs_folder_path = os.path.expanduser(folder_name)
    os.makedirs(abs_folder_path)
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
            s_dict['file'] = 'signal-{}{}.txt'.format(mn, sn)
            np.savetxt("{}/signal-{}{}.txt".format(abs_folder_path, mn, sn), s.x, fmt='%f')            
            m_dict['signals'].append(s_dict)
        e_dict['measurements'].append(m_dict)
                           
    s = json.dumps(e_dict, ensure_ascii=False, indent='    ')
    with open('{}/info.json'.format(abs_folder_path), 'w') as f:
        f.write(s)
