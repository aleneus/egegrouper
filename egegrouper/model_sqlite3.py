import sqlite3
import numpy as np
from collections import OrderedDict

from egegrouper.model import *
from egegrouper import sqlite3_scripts

class GrouperModelSqlite3(GrouperModel):
    """Model implementation for SQLite3 SME data base."""
    
    def __init__(self):
        super().__init__()
        self.conn = None
        self.c = None

    def create_storage(self, file_name):
        """Create new data base.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if self.storage_opened():
            self.close_storage()
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.c.executescript(sqlite3_scripts.create_sme_db)
        self.conn.commit()
        self.set_storage_opened(True)

    def open_storage(self, file_name):
        """Open data base.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if self.storage_opened():
            self.close_storage()
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.c.execute("pragma foreign_keys=on")
        self.set_storage_opened(True)

    def close_storage(self):
        """Close data base."""
        self.conn.close()
        self.set_storage_opened(False)

    def get_examination(self, exam_id):
        """Return examination from data base.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        Returns
        -------
        sme.Examination
            Examination object.

        """
        try:
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
                SELECT S.dt, S.data FROM signal AS S
                WHERE meas_id = ? """, [m_id, ]))
                for s_sql in ss_sql:
                    s = Signal()
                    s.dt = s_sql[0]
                    s.x = np.array(np.frombuffer(s_sql[1]))
                    m.ss.append(s)
                e.ms.append(m)
            return e
        except Exception:
            return None

    def insert_examination(self, e):
        """Insert examination into data base.

        Parameters
        ----------
        e : sme.Examination
            Examination object

        """
        exam_id = list(self.c.execute("""
        SELECT max(exam_id)
        FROM examination """))[0][0]
        if not exam_id:
            exam_id = 0
            
        meas_id = list(self.c.execute("""
        SELECT max(meas_id)
        FROM measurement """))[0][0]
        if not meas_id:
            meas_id = 0

        self.c.execute("""
        INSERT INTO examination (name, diagnosis, age, gender)
        VALUES (?,?,?,?) """, (e.name, e.diagnosis, e.age, e.gender) )
        exam_id += 1

        for m in e.ms:
            self.c.execute("""
            INSERT INTO measurement (time, exam_id)
            VALUES (?,?) """, (m.time, exam_id) )
            meas_id += 1

            for s in m.ss:
                self.c.execute("""
                INSERT INTO signal (data, dt, meas_id)
                VALUES (?,?,?) """, (s.x.tobytes(), s.dt, meas_id) )
            
        self.conn.commit()

    def storage_info_new(self):
        """Return tabular information about storage.

        Return
        ------
        ext_data : list of tuples
            Table with information about storage.
        ext_headers : tuple
            Headers.

        """
        # group records
        data = list(self.c.execute("""
        SELECT * FROM egeg_group;
        """))
        headers = tuple(map(lambda x: x[0], self.c.description))
        # number of examinations in groups
        num_in_groups = []

        ext_data = []
        for d in data:
            n = list(self.c.execute("""
            SELECT COUNT(E.exam_id)
            FROM examination as E, group_element as GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ? """, [d[0], ]))[0][0]
            ext_data.append(d + (n,))
        ext_headers = headers + ("number",)

        ungrouped_num = list(self.c.execute("""
        SELECT COUNT(exam_id)
        FROM examination
        WHERE exam_id NOT IN (SELECT exam_id FROM group_element) """, []))[0][0]

        last_string = ['' for h in ext_headers[0]]
        last_string[0] = '0'
        last_string[-2] = 'Ungrouped'
        last_string[-1] = ungrouped_num
        ext_data.append(tuple(last_string))
        
        return ext_data, ext_headers
    
    def storage_info(self):
        """Return information about storage.
        
        Returns
        -------
        exams_total_num : int 
            Total number of examinations.
        data : list of tuples
            Group description.
        num_in_groups : list
            Number of examination in every group.
        ungrouped_num : int 
            Number of ungrouped examinations.

        """
        # total number of examinations
        q = """
        SELECT count(*)
        FROM examination """
        exams_num = list(self.c.execute(q, []))[0][0]
        # fields from db
        q = """
        SELECT *
        FROM egeg_group """
        data = list(self.c.execute(q, []))
        # numbers of exams in groups
        num_in_groups = []
        for d in data:
            q = """
            SELECT COUNT(E.exam_id)
            FROM examination as E, group_element as GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ? """
            num_in_groups.append(list(self.c.execute(q, [d[0], ]))[0][0])
        # number of ungrouped examinations
        q = """
        SELECT COUNT(exam_id)
        FROM examination
        WHERE exam_id NOT IN (SELECT exam_id FROM group_element) """
        ungrouped_num = list(self.c.execute(q, []))[0][0]
        return exams_num, data, num_in_groups, ungrouped_num

    def group_info(self, group_id):
        """Return short information about examinations in selected group.

        Parameters
        ----------
        group_id : str
            Group ID

        Returns
        -------
        data : list of tuple
            Examination descriptions.
        headers : tuple
            Headers.

        """
        if group_id == '0':
            data = list(self.c.execute("""
            SELECT exam_id, name, diagnosis, age, gender
            FROM examination
            WHERE exam_id NOT IN (SELECT exam_id FROM group_element) 
            """, []))
        else:
            data = list(self.c.execute("""
            SELECT E.exam_id, E.name, E.diagnosis, E.age, E.gender
            FROM examination AS E, group_element AS GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ?
            """, [group_id, ]))

        headers = tuple(map(lambda x: x[0], self.c.description))

        return data, headers

    def insert_group(self, name, description):
        """Add new group of examinations.

        Parameters
        ----------
        name : str
            Name of new group.
        description : str
            Description for new group.

        """
        self.c.execute("""
        INSERT INTO egeg_group (name, description)
        VALUES (?, ?) """, [name, description, ])
        self.conn.commit()

    def delete_group(self, group_id):
        """Delete group of examinations fron data base.

        Parameters
        ----------
        group_id : str
            Group ID.
        """
        self.c.execute("""
        DELETE FROM egeg_group
        WHERE group_id = ? """, [group_id, ])
        self.conn.commit()

    def add_exam_to_group(self, exam_id, group_id):
        """Add examination into group.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        group_id : str
            Group ID.

        """
        try:
            self.c.execute("""
            INSERT OR REPLACE INTO group_element
            VALUES (?, ?) """, [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def delete_exam_from_group(self, exam_id, group_id):
        """Delete examination from group.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        group_id : str
            Group ID.

        """
        try:        
            self.c.execute("""
            DELETE FROM group_element
            WHERE exam_id = ? AND group_id = ? """, [exam_id, group_id, ])
            self.conn.commit()
        except sqlite3.IntegrityError:
            print('Error: no such examination or group')

    def where_is_examination(self, exam_id):
        """Return groups numbers and names where examination is.

        Returns
        -------
        list of tuples

        """
        data = list(self.c.execute("""
        SELECT G.group_id, G.name
        FROM egeg_group as G, group_element
        WHERE G.group_id = group_element.group_id AND group_element.exam_id = ? """, [exam_id]))
        return data

    def add_sme_db(self, file_name):
        """Add SME sqlite3 data base to current data base.

        Parameters
        ----------
        file_name : str
            Name of file with SQLite3 SME data base.

        """
        source_name = file_name
        dest_name = self.file_name
        if self.storage_opened():
            self.close_storage()
        SMEDBImporter().DBimport(dest_name, source_name)
        self.open_storage(dest_name)

    def add_gs_db(self, file_name):
        """Add GS sqlite3 data base to current data base.
        
        Parameters
        ----------
        file_name : str
            Name of file with SQLite3 Gastroscan data base.

        """
        source_name = file_name
        dest_name = self.file_name
        if self.storage_opened():
            self.close_storage()
        GSDBImporter().DBimport(dest_name, source_name)
        self.open_storage(dest_name)

    def add_exam_from_json_folder(self, folder_name):
        """Add examination from JSON folder to current data base.

        Parameters
        ----------
        folder_name : str
            Name of folder with info.json and signal txt files.
        
        """
        try:
            e = get_exam_from_folder(folder_name)
            self.insert_examination(e)
            return True
        except Exception: #FileNotFoundError:
            return False

    def export_as_json_folder(self, exam_id, folder_name):
        """Export examination to JSON folder. Return True if sucsess, False overwise.
        
        Parameters
        ----------
        folder_name : str
            Name of folder for export info.json and signals in txt format.
        
        """
        e = self.get_examination(exam_id)
        return put_exam_to_folder(e, folder_name)

    def delete_exam(self, exam_id):
        """Remove examination from data base.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        """
        self.c.execute("""
        DELETE FROM Examination
        WHERE exam_id = ?
        """,(exam_id, ))
        self.conn.commit()

    def group_record(self, group_id):
        """Return attribute names and values of selected group.

        Parameters
        ----------
        group_id : str
            Group ID.

        Returns
        -------
        : OrderedDict
            Attributes names and values for selected group.
        """
        attr = OrderedDict()
        try:
            attr['name'], attr['description'] = list(self.c.execute("""
            SELECT name, description
            FROM egeg_group
            WHERE group_id = ?
            """, (group_id, )))[0]
            return attr
        except IndexError:
            return None

    def update_group_record(self, group_id, attr):
        """Update group record in data base. Return True if sucsess, False overwise.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        """
        try:
            self.c.execute("""
            UPDATE egeg_group
            SET name = ?, description = ?
            WHERE group_id = ?
            """, (attr['name'], attr['description'], group_id, ))
            self.conn.commit()
            return True
        except Exceprtion:
            return False
