import json
import os

from sme import *

def get_exam_from_folder(folder_name):
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
    # create folder
    if os.path.exists(folder_name):
        return 1 # folder exists
    
    os.makedirs(folder_name)
    # form signals
    mn = 0
    for m in e.ms:
        mn += 1
        sn = 0
        for s in m.ss:
            sn += 1
            np.savetxt("{}/signal-{}{}.txt".format(folder_name, mn, sn), s.x)
        
    # form info.json
    to_json = {
        "name" : e.name,
        "diagnosis" : e.diagnosis,
        "age" : e.age,
        "gender" : e.gender,
        "measurements" : [
            {
                "time" : m.time,
                "signals" : [
                    {"dt" : s.dt, "file" : "signal-{}{}.txt".format(mn, sn)}
                    for s, sn in zip(m.ss, range(1, len(m.ss) + 1))
                ]
            } for m, mn in zip(e.ms, range(1, len(e.ms) + 1))
        ]
    }
    s = json.dumps(to_json, ensure_ascii=False, indent='    ')
    with open('{}/info.json'.format(folder_name), 'w') as f:
        f.write(s)
    return 0
