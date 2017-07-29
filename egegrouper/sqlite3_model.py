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

import sqlite3
import numpy as np
from collections import OrderedDict
import os

from .base_model import BaseModel
from . import sme
from . import sme_sqlite3
from . import sme_json

class Model(BaseModel):
    """Model implementation for SQLite3 SME database."""
    
    def __init__(self):
        """Constructor.
        
        Create fields and set initial state of model.
        
        """
        super().__init__()
        self.conn = None
        self.c = None
        self.set_state(storage_opened=False, file_name = None)

    def create_storage(self, file_name):
        """Create new database.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if self.state()['storage_opened']:
            self.close_storage()
        abs_file_name = os.path.expanduser(file_name)
        if os.path.isfile(abs_file_name):
            os.remove(abs_file_name)
        self.conn = sqlite3.connect(abs_file_name)
        self.c = self.conn.cursor()
        self.c.executescript(create_sme_db_script)
        self.conn.commit()
        self.set_state(storage_opened=True, file_name = abs_file_name)

    def open_storage(self, file_name):
        """Open database.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if self.state()['storage_opened']:
            self.close_storage()
        abs_file_name = os.path.expanduser(file_name)
        self.conn = sqlite3.connect(abs_file_name)
        self.c = self.conn.cursor()
        self.c.execute("pragma foreign_keys=on")
        self.set_state(storage_opened=True, file_name=abs_file_name)

    def close_storage(self):
        """Close current database."""
        if self.state()['storage_opened']:
            self.conn.close()
            self.set_state(storage_opened=False, file_name=None)

    def storage_exists(self, file_name):
        """Check if the file exists.

        Parameters
        ----------
        file_name : str
            Name of database file.

        Returns
        -------
        : bool
            True if exists, False otherwise.

        """
        abs_file_name = os.path.expanduser(file_name)
        return os.path.isfile(abs_file_name)

    @BaseModel.do_if_storage_opened
    def exam(self, exam_id):
        """Return examination from database.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        Returns
        -------
        sme.Examination
            Examination object.

        """
        return sme_sqlite3.get_exam(self.conn, exam_id)

    @BaseModel.do_if_storage_opened
    def insert_exam(self, exam):
        """Insert examination into current database.

        Parameters
        ----------
        exam : sme.Examination
            Examination object

        """
        sme_sqlite3.put_exam(self.conn, exam)

    @BaseModel.do_if_storage_opened
    def exams(self, group_id):
        """
        Return examinations of selected group.

        Parameters
        ----------
        group_id : str
           Group ID.

        Returns
        -------
        : list of sme.Examination
            Examination objects.
        
        """
        exam_records, headers = self.group_info(group_id)
        if exam_records == None:
            return None
        return [
            self.exam(exam_record[0])
            for exam_record
            in exam_records
        ]

    @BaseModel.do_if_storage_opened
    def extract_exams(self, group_ids, operation = 'union'):
        """
        Return examinations of selected groups.

        Parameters
        ----------
        group_ids : list of str
           Group IDs. Group id equals to '0' means ungrouped examinations.
        operation : str
           Operation under selected sets (groups) of examinations. Must be 'union' or 'intersect'. Default is 'union'.

        Returns
        -------
        : list of sme.Examination
            Examination objects.
        
        """

        # get list of exam_ids using SQL
        if operation == 'union':
            word = "UNION"
        elif operation == 'intersect':
            word = "INTERSECT"
        else:
            return None
            
        def build_select_part(group_id):
            if group_id == '0':
                select_part = """
                SELECT exam_id
                FROM examination
                WHERE exam_id NOT IN (SELECT exam_id FROM group_element)
                """
            else:
                select_part = """
                SELECT E.exam_id from examination as E JOIN group_element as GE ON E.exam_id = GE.exam_id 
                WHERE GE.group_id = ?
                """
            return select_part

        full_query = ""
        for group_id in group_ids[:-1]:
            full_query += build_select_part(group_id) + word
        full_query += build_select_part(group_ids[-1]) + ';'

        non_zero_group_ids = []
        for group_id in group_ids:
            if group_id != '0':
                non_zero_group_ids.append(group_id)
                
        self.c.execute(full_query, non_zero_group_ids)

        exam_ids = []
        for row in self.c.fetchall():
            exam_ids.append(row[0])
        
        # get list of exams using mapping module
        if len(exam_ids) == 0:
            return None
        return [
            self.exam(exam_id)
            for exam_id
            in exam_ids
        ]

    @BaseModel.do_if_storage_opened
    def delete_exam(self, exam_id):
        """Remove examination from database.

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

    @BaseModel.do_if_storage_opened
    def storage_info(self):
        """Return tabular information about database.

        Returns
        -------
        ext_data : list of tuple
            Table with information about database.
        ext_headers : tuple
            Headers.

        """
        self.c.execute("""
        SELECT * FROM egeg_group;
        """)
        data = self.c.fetchall()
        headers = tuple(map(lambda x: x[0], self.c.description))
        num_in_groups = []

        ext_data = []
        for d in data:
            self.c.execute("""
            SELECT COUNT(E.exam_id)
            FROM examination as E, group_element as GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ? """, [d[0], ])
            n = self.c.fetchall()[0][0]
            ext_data.append(d + (n,))
        ext_headers = headers + ("number",)

        self.c.execute("""
        SELECT COUNT(exam_id)
        FROM examination
        WHERE exam_id NOT IN (SELECT exam_id FROM group_element) """)
        ungrouped_num = self.c.fetchall()[0][0]
        
        last_string = ['' for h in ext_headers]
        last_string[0] = '0'
        last_string[-2] = 'Ungrouped'
        last_string[-1] = ungrouped_num
        ext_data.append(tuple(last_string))
        
        return ext_data, ext_headers    

    @BaseModel.do_if_storage_opened
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
            self.c.execute("""
            SELECT exam_id, name, diagnosis, age, gender
            FROM examination
            WHERE exam_id NOT IN (SELECT exam_id FROM group_element) 
            """)
        else:
            self.c.execute("""
            SELECT COUNT(*) FROM egeg_group WHERE group_id = ?
            """, [group_id])
            if self.c.fetchall()[0][0] == 0:
                return None, None

            self.c.execute("""
            SELECT E.exam_id, E.name, E.diagnosis, E.age, E.gender
            FROM examination AS E, group_element AS GE
            WHERE GE.exam_id = E.exam_id AND GE.group_id = ?
            """, [group_id, ])
            
        data = self.c.fetchall()
        headers = tuple(map(lambda x: x[0], self.c.description))
        return data, headers

    @BaseModel.do_if_storage_opened
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

    @BaseModel.do_if_storage_opened
    def delete_group(self, group_id):
        """Delete group of examinations from database.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        self.c.execute("""
        DELETE FROM egeg_group
        WHERE group_id = ? """, [group_id, ])
        self.conn.commit()

    @BaseModel.do_if_storage_opened
    def group_exam(self, exam_id, group_ids, placed_in):
        """Add and delete examination to and from groups.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        group_ids : list of str
            Group IDs.
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

    @BaseModel.do_if_storage_opened
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
            True if exam in group, False otherwise.
        
        """

        including_exam_groups_ids = [
            r[0] for r in self.c.execute("""
            SELECT G.group_id
            FROM egeg_group as G, group_element
            WHERE G.group_id = group_element.group_id AND group_element.exam_id = ? """, [exam_id])
        ]

        self.c.execute("SELECT * FROM egeg_group")
        group_records = self.c.fetchall()
        headers = tuple(map(lambda x: x[0], self.c.description))
        placed_in = [gr[0] in including_exam_groups_ids for gr in group_records]
        
        return group_records, headers, placed_in

    @BaseModel.do_if_storage_opened
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
        self.c.execute("""
        SELECT name, description
        FROM egeg_group
        WHERE group_id = ?
        """, (group_id, ))
        attr['name'], attr['description'] = self.c.fetchone()
        return attr

    @BaseModel.do_if_storage_opened
    def update_group_record(self, group_id, attr):
        """Update group record in database.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        """
        self.c.execute("""
        UPDATE egeg_group
        SET name = ?, description = ?
        WHERE group_id = ?
        """, (attr['name'], attr['description'], group_id, ))
        self.conn.commit()

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
