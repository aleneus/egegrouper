import json
import numpy as np

class Signal:
    def __init__(self):
        self.dt = None
        self.edited = None
        self.x = []

class Measurement:
    def __init__(self):
        self.time = None
        self.ss = []
        
class Examination:
    def __init__(self):
        self.name = None
        self.age = None
        self.gender = None
        self.diagnosis = None
        self.ms = []

    def get_from_json_folder(self, folder_name):
        with open('{}/info.json'.format(folder_name), 'r') as f:
            data = json.load(f)
            
        self.name = data['name']
        self.age = data['age']
        self.gender = data['gender']
        self.diagnosis = data['diagnosis']
        self.ms = []
        for m_data in data['measurements']:
            m = Measurement()
            m.time = m_data['time']
            m.ss = []
            for s_data in m_data['signals']:
                s = Signal()
                s.dt = s_data['dt']
                s.x = np.loadtxt('{}/{}'.format(folder_name, s_data['file']))
                m.ss.append(s)
            self.ms.append(m)

    def put_to_json_folder(self, folder_name):
        # form signals
        mn = 0
        for m in self.ms:
            mn += 1
            sn = 0
            for s in m.ss:
                sn += 1
                np.savetxt("{}/signal-{}{}.txt".format(folder_name, mn, sn), s.x)
        
        # form info.json
        to_json = {
                   "name" : self.name,
                   "diagnosis" : self.diagnosis,
                   "age" : self.age,
                   "gender" : self.gender,
                   "measurements" : [
                       {
                        "time" : m.time,
                        "signals" : [
                            {"dt" : s.dt, "file" : "signal-{}{}.txt".format(mn, sn)}
                            for s, sn in zip(m.ss, range(1, len(m.ss) + 1))
                        ]
                       } for m, mn in zip(self.ms, range(1, len(self.ms) + 1))
                   ]
        }
        s = json.dumps(to_json, ensure_ascii=False, indent='    ')
        with open('{}/info.json'.format(folder_name), 'w') as f:
            f.write(s)
