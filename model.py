import sqlite3
import numpy as np
from DBImport import *

def blob2ndarray(signal_blob):
    datatype = np.dtype(float)
    datatype = datatype.newbyteorder('>')
    return np.array(np.frombuffer(signal_blob))

class Examination:
    def __init__(self):
        self.ms = []

class Measurement:
    def __init__(self):
        self.ss = []

class Signal:
    def __init__(self):
        self.x = []

class GrouperModel:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.fname = None

    """ Work with DB
    """

    def db_opened(self):
        return self.conn != None
    
    def open_db(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.c.execute("pragma foreign_keys=on")
        self.fname = file_name

    def close_db(self):
        self.conn.close()
        self.conn = None
        self.fname = None

    def create_db(self, fname):
        if self.db_opened():
            self.close_db()
        self.conn = sqlite3.connect(fname)
        self.c = self.conn.cursor()
        script = open('Create_SME_DB.sql', 'r').read()
        self.c.executescript(script)
        self.conn.commit()

    def add_data_from_sme(self, fname):
        source_name = fname
        dest_name = self.fname
        if self.db_opened():
            self.close_db()
        SMEDBImporter().DBimport(dest_name, source_name)
        self.open_db(dest_name)


    """ Work with data
    """

    def __select(self, query, args):
        res = list(self.c.execute(query, args))
        return res

    def db_info(self):
        # number of groups
        q = "select count(*)\
             from egeg_group;"
        groups_num = list(self.__select(q, []))[0][0]
        # total number of examinations
        q = "select count(*)\
             from examination"
        exams_total_num = list(self.__select(q, []))[0][0]
        # fields from db
        q = "select *\
             from egeg_group;"
        fields = list(self.__select(q, []))
        # numbers of exams in groups
        num_in_groups = []
        for f in fields:
            q = "select count(E.exam_id)\
                 from examination as E, group_element as GE\
                 where GE.exam_id = E.exam_id and GE.group_id = ?"
            num_in_groups.append(list(self.__select(q, [f[0], ]))[0][0])
        # number of ungrouped examinations
        q = 'select count(exam_id)\
             from examination\
             where exam_id not in (select exam_id from group_element)'
        ungrouped_num = list(self.__select(q, []))[0][0]
        return [exams_total_num, groups_num, fields, num_in_groups, ungrouped_num]

    def group_info(self, group_id):
        if group_id == '0':
            q = 'select exam_id, name, diagnosis, age, gender\
                 from examination\
                 where exam_id not in (select exam_id from group_element)'
            return list(self.__select(q, []))
            
        q = "select E.exam_id, E.name, E.diagnosis, E.age, E.gender\
             from examination as E, group_element as GE\
             where GE.exam_id = E.exam_id and GE.group_id = ?\
             order by E.name;"
        return list(self.__select(q, [group_id, ]))

    def exam_info(self, exam_id):
        q = "select M.meas_id, M.time from measurement as M\
             where M.exam_id = ?;"
        return list(self.__select(q, [exam_id, ]))

    def exam_info_test(self, exam_id):
        m = ('123', '11-12-2013', '19.00.15')
        s = ('234', 'source', '40 m', '2 Hz', 'Q=0.56')
        e = ('10', 'Ivanov', 'Normal', 'm', '78')
        res = (e, [(m,[s,s]),(m,[s,s])])
        return res

    def get_examination(self, exam_id):
        e = Examination()
        ms = []
        q = "select * from measurement\
             where exam_id = ?\
             order by meas_id"
        ms_sql = list(self.__select(q, [exam_id, ]))
        for m_sql in ms_sql:
            m = Measurement()
            ss = []
            q = "select * from signal\
                 where meas_id = ?\
                 order by edited"
            ss_sql = list(self.__select(q, [m_sql[0], ]))
            for s_sql in ss_sql:
                s = Signal()
                s.x = blob2ndarray(s_sql[1])
                ss.append(s)
            m.ss = ss
            ms.append(m)
        e.ms = ms
        return e

    def insert_group(self, name, description):
        q = "insert into egeg_group (name, description) values (?, ?)"
        self.c.execute(q, [name, description, ])
        self.conn.commit()

    def delete_group(self, group_id):
        q = "delete from egeg_group where group_id = ?"
        self.c.execute(q, [group_id, ])
        self.conn.commit()

    def add_to_group(self, exam_id, group_id):
        try:
            q = "insert or replace into group_element values (?, ?)"
            self.c.execute(q, [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def delete_from_group(self, exam_id, group_id):
        try:        
            q = "delete from group_element where exam_id = ? and group_id = ?"
            self.c.execute(q, [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def where_is_examination(self, exam_id):
        q = "SELECT G.group_id, G.name\
             FROM egeg_group as G, group_element\
             WHERE G.group_id = group_element.group_id AND group_element.exam_id = ?"
        data = list(self.c.execute(q, [exam_id]))
        return data
