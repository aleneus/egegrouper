import sqlite3
import numpy as np
import os

from sme import *
from DBImport import *
from sme_json_folders import *

def blob2ndarray(signal_blob):
    return np.array(np.frombuffer(signal_blob))

def ndarry2blob(signal_ndarray):
    return signal_ndarray.tobytes()

class GrouperModel:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.fname = None

    """ Work with DB
    """

    def db_opened(self):
        return self.conn != None
    
    def create_db(self, fname):
        if self.db_opened():
            self.close_db()
        self.conn = sqlite3.connect(fname)
        self.c = self.conn.cursor()
        script = open('sqlite_scripts/Create_SME_DB.sql', 'r').read()
        self.c.executescript(script)
        self.conn.commit()
        self.fname = fname

    def open_db(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.c.execute("pragma foreign_keys=on")
        self.fname = file_name

    def close_db(self):
        self.conn.close()
        self.conn = None
        self.fname = None

    """ Mapping
    """
    
    def get_examination(self, exam_id):
        e = Examination()
        e.name, e.diagnosis, e.age, e.gender = list(self.c.execute("""
        SELECT E.name, E.diagnosis, E.age, E.gender FROM examination AS E
        WHERE exam_id = ? """, [exam_id, ]))[0]
        e.ms = []
        ms_sql = list(self.c.execute("""
        SELECT M.meas_id, M.time FROM measurement AS M
        WHERE exam_id = ?
        ORDER BY meas_id """, [exam_id, ]))
        for m_sql in ms_sql:
            m = Measurement()
            m_id, m.time = m_sql
            m.ss = []
            ss_sql = list(self.c.execute("""
            SELECT S.dt, S.edited, S.data FROM signal AS S
            WHERE meas_id = ?
            ORDER BY edited """, [m_id, ]))
            for s_sql in ss_sql:
                s = Signal()
                s.dt, s.edited = s_sql[:-1]
                s.x = blob2ndarray(s_sql[-1])
                m.ss.append(s)
            e.ms.append(m)
        return e

    def insert_examination(self, e):
        exam_id = list(self.c.execute("""
        SELECT max(exam_id)
        FROM examination
        """))[0][0]
        if not exam_id:
            exam_id = 0
            
        meas_id = list(self.c.execute("""
        SELECT max(meas_id)
        FROM measurement
        """))[0][0]
        if not meas_id:
            meas_id = 0

        self.c.execute("""
        INSERT INTO examination (name, diagnosis, age, gender)
        VALUES (?,?,?,?)
        """, (e.name, e.diagnosis, e.age, e.gender) )
        exam_id += 1

        for m in e.ms:
            self.c.execute("""
            INSERT INTO measurement (time, exam_id)
            VALUES (?,?)
            """, (m.time, exam_id) )
            meas_id += 1

            for s in m.ss:
                self.c.execute("""
                INSERT INTO signal (data, dt, edited, meas_id)
                VALUES (?,?,?,?)
                """, (ndarry2blob(s.x), s.dt, 0, meas_id) )
            
        self.conn.commit()

    """ Data Viewing
    """

    def db_info(self):
        # number of groups
        q = """
        SELECT count(*)
        FROM egeg_group
        """
        groups_num = list(self.c.execute(q, []))[0][0]
        # total number of examinations
        q = """
        SELECT count(*)
        FROM examination
        """
        exams_total_num = list(self.c.execute(q, []))[0][0]
        # fields from db
        q = """
        SELECT *
        FROM egeg_group
        """
        fields = list(self.c.execute(q, []))
        # numbers of exams in groups
        num_in_groups = []
        for f in fields:
            q = """
            SELECT COUNT(E.exam_id)
            FROM examination as E, group_element as GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ?
            """
            num_in_groups.append(list(self.c.execute(q, [f[0], ]))[0][0])
        # number of ungrouped examinations
        q = """
        SELECT COUNT(exam_id)
        FROM examination
        WHERE exam_id NOT IN (SELECT exam_id FROM group_element)
        """
        ungrouped_num = list(self.c.execute(q, []))[0][0]
        return [exams_total_num, groups_num, fields, num_in_groups, ungrouped_num]

    def group_info(self, group_id):
        if group_id == '0':
            return list(self.c.execute("""
            SELECT exam_id, name, diagnosis, age, gender
            FROM examination
            WHERE exam_id NOT IN (SELECT exam_id FROM group_element)
            """, []))
            
        return list(self.c.execute("""
        SELECT E.exam_id, E.name, E.diagnosis, E.age, E.gender
        FROM examination AS E, group_element AS GE
        WHERE GE.exam_id = E.exam_id AND GE.group_id = ?
        ORDER BY E.name
        """, [group_id, ]))

    def exam_info(self, exam_id):
        e = list(self.c.execute("""
        SELECT * FROM examination
        WHERE exam_id = ?
        """, [exam_id, ]))[0]
        s = ('234', 'source', '40 m', '2 Hz', 'Q=0.56')
        ms = []
        ms_sql = list(self.c.execute("""
        SELECT meas_id, time FROM measurement
        WHERE exam_id = ?
        ORDER BY meas_id
        """, [exam_id, ]))
        for m in ms_sql:
            ss = []
            ss = list(self.c.execute("""
            SELECT signal_id, edited FROM signal
            WHERE meas_id = ?
            ORDER BY edited
            """, [m[0], ]))
            ms.append((m, ss))
     
        res = (e, ms)
        return res

        
    """ Grouping
    """
    
    def insert_group(self, name, description):
        self.c.execute("\
        INSERT INTO egeg_group (name, description)\
        VALUES (?, ?)\
        ", [name, description, ])
        self.conn.commit()

    def delete_group(self, group_id):
        q = ""
        self.c.execute("\
        DELETE FROM egeg_group\
        WHERE group_id = ?\
        ", [group_id, ])
        self.conn.commit()

    def add_exam_to_group(self, exam_id, group_id):
        try:
            self.c.execute("\
            INSERT OR REPLACE INTO group_element\
            VALUES (?, ?)\
            ", [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def delete_from_group(self, exam_id, group_id):
        try:        
            self.c.execute("\
            DELETE FROM group_element\
            WHERE exam_id = ? AND group_id = ?\
            ", [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def where_is_examination(self, exam_id):
        data = list(self.c.execute("\
        SELECT G.group_id, G.name\
        FROM egeg_group as G, group_element\
        WHERE G.group_id = group_element.group_id AND group_element.exam_id = ?\
        ", [exam_id]))
        return data


    """ Import and export
    """

    def add_sme_db(self, fname):
        source_name = fname
        dest_name = self.fname
        if self.db_opened():
            self.close_db()
        SMEDBImporter().DBimport(dest_name, source_name)
        self.open_db(dest_name)

    def add_gs_db(self, fname):
        source_name = fname
        dest_name = self.fname
        if self.db_opened():
            self.close_db()
        GSDBImporter().DBimport(dest_name, source_name)
        self.open_db(dest_name)

    def add_exam_from_json_folder(self, folder_name):
        e = get_exam_from_folder(folder_name)
        self.insert_examination(e)

    def export_as_json_folder(self, exam_id, folder_name):
        e = self.get_examination(exam_id)
        put_exam_to_folder(e, folder_name)
