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

# TODO: add to doc

import sqlite3
from . import sme
import numpy as np

def get_exam(cursor, exam_id):
    """TODO

    """
    e = sme.Examination()
    cursor.execute("""
    SELECT E.name, E.diagnosis, E.age, E.gender FROM examination AS E
    WHERE exam_id = ? """, [exam_id, ])
    result = cursor.fetchone()
    if not result:
        return None
    e.name, e.diagnosis, e.age, e.gender = result
    e.ms = []
    cursor.execute("""
    SELECT M.meas_id, M.time FROM measurement AS M
    WHERE exam_id = ?
    ORDER BY meas_id """, [exam_id, ])
    for m_sql in cursor.fetchall():
        m = sme.Measurement()
        m_id, m.time = m_sql
        m.ss = []
        cursor.execute("""
        SELECT S.dt, S.data FROM signal AS S
        WHERE meas_id = ? """, [m_id, ])
        for s_sql in cursor.fetchall():
            s = sme.Signal()
            s.dt = s_sql[0]
            s.x = np.array(np.frombuffer(s_sql[1]))
            m.ss.append(s)
        e.ms.append(m)
    return e

def put_exam(cursor, exam):
    """TODO

    """
    cursor.execute("""
    SELECT max(exam_id)
    FROM examination """)
    exam_id = cursor.fetchone()[0]
    if not exam_id:
        exam_id = 0

    cursor.execute("""
    SELECT max(meas_id)
    FROM measurement """)
    meas_id = cursor.fetchone()[0]
    if not meas_id:
        meas_id = 0

    cursor.execute("""
    INSERT INTO examination (name, diagnosis, age, gender)
    VALUES (?,?,?,?) """, (exam.name, exam.diagnosis, exam.age, exam.gender) )
    exam_id += 1

    for m in exam.ms:
        cursor.execute("""
        INSERT INTO measurement (time, exam_id)
        VALUES (?,?) """, (m.time, exam_id) )
        meas_id += 1

        for s in m.ss:
            cursor.execute("""
            INSERT INTO signal (data, dt, meas_id)
            VALUES (?,?,?) """, (s.x.tobytes(), s.dt, meas_id) )
