import json
import numpy as np

class Signal:
    def __init__(self):
        self.dt = None
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

    def get_from_json_file(self, folder_name):
        with open('{}/info.json'.format(folder_name)) as f:
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
             
    def print(self):
        print()
        print('name = {}'.format(self.name))
        print('age = {}'.format(self.age))
        print('gender = {}'.format(self.gender))
        print('diagnosis = {}'.format(self.diagnosis))
        for m in self.ms:
            print('    {}'.format(m.time))
            for s in m.ss:
                print('        {}'.format(s.dt))
                print('        {}'.format(len(s.x)))
        print()
