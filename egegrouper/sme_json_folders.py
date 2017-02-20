"""Mapping examinations to and from JSON folders."""

import json
import os
from collections import OrderedDict

from egegrouper.sme import *

def get_exam_from_folder(folder_name):
    """Get examination object from folder with file info.json.
    
    Return
    ------
    : sme.Examination
        Examination instance.

    """
    e = Examination()
    with open('{}/info.json'.format(folder_name), 'r') as f:
        data = json.load(f)
            
    e.name = data['name']
    e.age = data['age']
    e.gender = data['gender']
    e.diagnosis = data['diagnosis']
    e.ms = []
    for m_data in data['measurements']:
        m = Measurement()
        m.time = m_data['time']
        m.ss = []
        for s_data in m_data['signals']:
            s = Signal()
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
    if os.path.exists(folder_name):
        return False

    os.makedirs(folder_name)
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
            np.savetxt("{}/signal-{}{}.txt".format(folder_name, mn, sn), s.x)            
            m_dict['signals'].append(s_dict)
        e_dict['measurements'].append(m_dict)
                           
    s = json.dumps(e_dict, ensure_ascii=False, indent='    ')
    with open('{}/info.json'.format(folder_name), 'w') as f:
        f.write(s)
    return True
