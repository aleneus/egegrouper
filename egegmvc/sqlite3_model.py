"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sqlite3
import numpy as np
from collections import OrderedDict
import os

from egegmvc.model import BaseModel
import egegmvc.sme as sme
import egegmvc.sme_json_folders as jsme

class Model(BaseModel):
    """Model implementation for SQLite3 SME data base."""
    
    def __init__(self):
        super().__init__()
        self.conn = None
        self.c = None
        self.set_state(storage_opened=False, file_name = None)

    def create_storage(self, file_name):
        """Create new data base.

        Parameters
        ----------
        file_name : str
            File name.

        Return
        ------
        : bool
            True if storage was created, False overwise.

        """
        if self.state()['storage_opened']:
            self.close_storage()
        if os.path.isfile(file_name):
            os.remove(file_name)
        try:
            self.conn = sqlite3.connect(file_name)
            self.c = self.conn.cursor()
            self.c.executescript(create_sme_db_script)
            self.conn.commit()
            self.set_state(storage_opened=True, file_name = file_name)
            return True
        except Exception:
            return False

    def open_storage(self, file_name):
        """Open data base.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if self.state()['storage_opened']:
            self.close_storage()
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.c.execute("pragma foreign_keys=on")
        self.set_state(storage_opened=True, file_name=file_name)
        return True

    def close_storage(self):
        """Close data base."""
        if self.state()['storage_opened']:
            self.conn.close()
        self.set_state(storage_opened=False, file_name=None)

    def storage_exists(self, file_name):
        """Check if storage exists.

        Returns
        -------
        : bool
            True if exists, False overwise.

        """
        return os.path.isfile(file_name)
    
    def exam(self, exam_id):
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
            e = sme.Examination()
            e.name, e.diagnosis, e.age, e.gender = list(self.c.execute("""
            SELECT E.name, E.diagnosis, E.age, E.gender FROM examination AS E
            WHERE exam_id = ? """, [exam_id, ]))[0]
            e.ms = []
            ms_sql = list(self.c.execute("""
            SELECT M.meas_id, M.time FROM measurement AS M
            WHERE exam_id = ?
            ORDER BY meas_id """, [exam_id, ]))
            for m_sql in ms_sql:
                m = sme.Measurement()
                m_id, m.time = m_sql
                m.ss = []
                ss_sql = list(self.c.execute("""
                SELECT S.dt, S.data FROM signal AS S
                WHERE meas_id = ? """, [m_id, ]))
                for s_sql in ss_sql:
                    s = sme.Signal()
                    s.dt = s_sql[0]
                    s.x = np.array(np.frombuffer(s_sql[1]))
                    m.ss.append(s)
                e.ms.append(m)
            return e
        except Exception:
            return None

    def insert_exam(self, e):
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

    def storage_info(self):
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

        last_string = ['' for h in ext_headers]
        last_string[0] = '0'
        last_string[-2] = 'Ungrouped'
        last_string[-1] = ungrouped_num
        ext_data.append(tuple(last_string))
        
        return ext_data, ext_headers    

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
        if not self.state()['storage_opened']:
            return
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

    def group_exam(self, exam_id, group_ids, placed_in):
        """Add and delete examination to and from groups.

        Parameters
        ----------
        exam_id : str
            Examination identifier.
        group_ids : list of str
            Group identifiers.
        placed_in : list of bool
            True for examinations to be placed in groups. Length of group_ids must be equal to length of placed_in.

        """
        for (group_id, p) in zip(group_ids, placed_in):
            if p:
                try:
                    self.c.execute("""
                    INSERT OR IGNORE INTO group_element
                    VALUES (?, ?) """, [exam_id, group_id, ])
                except sqlite3.IntegrityError:
                    pass
            else:
                try:
                    self.c.execute("""
                    DELETE FROM group_element
                    WHERE exam_id = ? AND group_id = ? """, [exam_id, group_id, ])
                except sqlite3.IntegrityError:
                    pass
        self.conn.commit()

    def where_exam(self, exam_id):
        """Return description of groups where examination in or not in.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        Returns
        -------
        group_records : list of tuple
            All group records.
        headers : list of str
            Names of group attributes.
        placed_in : list of bool
            True if exam in group, False overwise.
        
        """
        
        including_exam_groups_ids = [
            r[0] for r in list(self.c.execute("""
            SELECT G.group_id
            FROM egeg_group as G, group_element
            WHERE G.group_id = group_element.group_id AND group_element.exam_id = ? """, [exam_id]))
        ]

        group_records = list(self.c.execute("""
        SELECT * FROM egeg_group
        """))
        headers = tuple(map(lambda x: x[0], self.c.description))
        placed_in = [gr[0] in including_exam_groups_ids for gr in group_records]
        
        return group_records, headers, placed_in
    
    def add_sme_db(self, file_name):
        """Add SME sqlite3 data base to current data base.

        Parameters
        ----------
        file_name : str
            Name of file with SQLite3 SME data base.

        """
        source_name = file_name
        dest_name = self.state()['file_name']
        if self.state()['storage_opened']:
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
        dest_name = self.state()['file_name']
        if self.state()['storage_opened']:
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
            e = jsme.get_exam_from_folder(folder_name)
            self.insert_exam(e)
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
        e = self.exam(exam_id)
        return jsme.put_exam_to_folder(e, folder_name)

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
        except Exception:
            return False


class DBImporter:
    def DBimport(self, dest_filename, source_filename):
        """
        Import data.
        """	
        self._source_filename = source_filename
        self._dest_filename = dest_filename
        self.run()

class SMEDBImporter(DBImporter):
    def run(self):
        self._dconn = sqlite3.connect(self._dest_filename)
        self._sconn = sqlite3.connect(self._source_filename)
        
        self._dest_c = self._dconn.cursor()
        self._src_c = self._sconn.cursor()
        self._dest_c.execute("attach database ? as 'source';", (self._source_filename,))
        self._dest_c.executescript(add_sme_db_script)
        self._dest_c.execute("detach database source;")
        self._dest_c.execute('drop table variable;')
        self._dconn.commit()
        
        self._sconn.close()
        self._dconn.close()

class GSDBImporter(DBImporter):
    def run(self):
        self._dconn = sqlite3.connect(self._dest_filename)
        self._sconn = sqlite3.connect(self._source_filename)
        
        self._dest_c = self._dconn.cursor()
        self._src_c = self._sconn.cursor()
		
        res = self._src_c.execute('\
        SELECT name, diagnosis, age, sex, date, signal, edited \
        FROM record as r, waveform as w\
        WHERE r.id = w.record_id\
        ')
        
        exam_id, meas_id = self._get_last_ids()
        ind = []
        t = []
        for r in res:
            if self._form_exam(r, t, ind):
                exam_id, meas_id = self._insert_exam(t, ind, exam_id, meas_id)
                t = []
                ind = []
                t.append(r)
                ind.append(1)
        self._insert_exam(t, ind, exam_id, meas_id)
        self._dconn.commit()
        
        self._sconn.close()
        self._dconn.close()
        
    def _get_last_ids(self):
        """
        Get during (last) measurement's and examination's id.
        
        """
        exam_id = list(self._dest_c.execute('SELECT max(exam_id) FROM examination'))[0][0]
        meas_id = list(self._dest_c.execute('SELECT max(meas_id) FROM measurement'))[0][0]
        if not exam_id:
            exam_id = 0
        if not meas_id:
            meas_id = 0
        return (exam_id, meas_id)

    def _insert_exam(self, t, ind, exam_id, meas_id):
        """
        Insert examination to destination DB. Data takes from temprorary lists t and ind.
        
        """
        dt = 0.5
        self._dest_c.execute('\
        INSERT INTO examination (name, diagnosis, age, gender)\
        VALUES (?,?,?,?)',(t[0][0],t[0][1],t[0][2],t[0][3]))
        exam_id += 1
        meas_id += 1
        self._dest_c.execute('\
        INSERT INTO measurement(time, exam_id)\
        VALUES (?,?)',(t[0][4],exam_id))
        self._dest_c.execute('\
        INSERT INTO signal(data, dt, edited,meas_id)\
        VALUES (?,?,?,?)',(t[0][5], dt, t[0][6],meas_id)) 
        if 2 in ind:
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited,meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(2)][5], dt, t[ind.index(2)][6],meas_id)) 
        if 3 in ind:
            self._dest_c.execute('\
            INSERT INTO measurement(time, exam_id)\
            VALUES (?,?)',(t[ind.index(3)][4],exam_id))
            meas_id += 1
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited, meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(3)][5], dt, t[ind.index(3)][6],meas_id)) 
        if 4 in ind:
            self._dest_c.execute('\
            INSERT INTO signal(data, dt, edited, meas_id)\
            VALUES (?,?,?,?)',(t[ind.index(4)][5], dt, t[ind.index(4)][6],meas_id)) 
        return (exam_id, meas_id)

    def _form_exam(self, r, t, ind):
        """
        Form temprorary lists t and ind.
        
        """
        if len(t) == 0:
            t.append(r)
            ind.append(1)
        else:
            if t[-1][0] == r[0] and t[-1][2] == r[2] and t[-1][3] == r[3] and t[-1][4][:9] == r[4][:9]:
                if ind[-1] == 1 and t[-1][4] == r[4]:
                    ind.append(2)
                elif ind[-1] == 1 or ind[-1] == 2:
                    ind.append(3)
                elif ind[-1] == 3:
                    ind.append(4)
                t.append(r)
                return False
            else:
                return True


#---------------------------------------
# sqlite3 scripts
#---------------------------------------

# create new SME data base 
create_sme_db_script = """
pragma foreign_keys=1;

create table signal(
	signal_id integer,
	data blob,
	dt real,
	edited integer, 
	meas_id integer references measurement(meas_id) on delete cascade, 
	primary key(signal_id)
);

create table measurement(
	meas_id integer, 
	time text, 
	exam_id integer references examination(exam_id) on delete cascade, 
	primary key(meas_id)
);

create table examination(
	exam_id integer, 
	name text,
	diagnosis text, 
	age integer, 
	gender text, 
	primary key(exam_id)
);

create table egeg_group(
	group_id integer, 
	name text, 
	description text,
	primary key(group_id)		
);

create table group_element(
	exam_id integer references examination(exam_id) on delete cascade, 
	group_id integer references egeg_group(group_id) on delete cascade, 
	primary key(exam_id, group_id)
);
"""

# import SME data base
add_sme_db_script = """
-- Create temporary table for variables and store max values of SMEP entities from nation db.
drop table if exists variable;
create table variable(name text primary key, value integer);
insert into variable(name, value) values('max_exam_id', (select coalesce(max(exam_id),0) from examination));
insert into variable(name, value) values('max_meas_id', (select coalesce(max(meas_id),0) from measurement));
insert into variable(name, value) values('max_group_id', (select coalesce(max(group_id),0) from egeg_group));

-- Paste groups with increased id to onation DB from source DB
insert into egeg_group(group_id, name, description) select group_id + (select value from variable where name = 'max_group_id'), name, description from source.egeg_group;

-- Paste examinations
insert into examination(exam_id, name, diagnosis, age, gender) select exam_id + (select value from variable where name = 'max_exam_id'), name, diagnosis,age,gender from source.examination;

-- Paste measurements
insert into measurement(meas_id, time, exam_id) select meas_id + (select value from variable where name = 'max_meas_id'), time, exam_id + (select value from variable where name = 'max_exam_id') from source.measurement;

-- Paste signals
insert into signal(data, dt, meas_id, edited) select data, dt, meas_id + (select value from variable where name = 'max_meas_id'), edited from source.signal;

-- Connect SMEP and groups
insert into group_element(exam_id, group_id) select exam_id+(select value from variable where name = 'max_exam_id'), group_id + (select value from variable where name = 'max_group_id') from source.group_element;
"""