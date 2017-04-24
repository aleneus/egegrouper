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

from abc import ABC, abstractmethod
import os
import sqlite3
import numpy as np

from . import sme
from . import sme_json
from . import sme_sqlite3

class BaseImporter(ABC):
    """Base class for importers."""
    
    def __init__(self, controller):
        """Constructor.

        Set controller to work with.
        
        """
        self.controller = controller

    def do_work(self, source):
        """Try import data from source and ask controller to put data into storage.
        
        Parameters
        ----------
        source : str
            Name of data source.
        
        """
        abs_file_name = os.path.expanduser(source)
        es = self._get_exams(abs_file_name)
        self.controller.import_exams(es)

    @abstractmethod
    def _get_exams(self, source):
        """Return exams from data source or None.

        Parameters
        ----------
        source : str
            Name of data source.

        Returns
        -------
        list of sme.Examination
            List of examinations.

        """
        pass
    

class JsonFileImporter(BaseImporter):
    """Importer from JSON file."""
    def _get_exams(self, source):
        exam = sme_json.get_exam(source)
        return [exam, ]

class SmeImporter(BaseImporter):
    """Importer from SME sqlite3 database."""
    def _get_exams(self, source):
        abs_file_name = os.path.expanduser(source)
        conn = sqlite3.connect(abs_file_name)
        c = conn.cursor()
        c.execute("SELECT exam_id from examination;")
        exams = []
        for r in c.fetchall():
            exam_id = r[0]
            exam = sme_sqlite3.get_exam(conn, exam_id)
            exams.append(exam)
        conn.close()
        return exams

class GsImporter(BaseImporter):
    """Importer from Gastroscan sqlite3 database."""
    def _get_exams(self, source):
        abs_file_name = os.path.expanduser(source)
        conn = sqlite3.connect(abs_file_name)
        c = conn.cursor()
        exams = []
        c.execute("""SELECT id, name, diagnosis, age, sex, date FROM record;""")
        for record_row in c.fetchall():
            e = sme.Examination()
            record_id = record_row[0]
            e.name = record_row[1]
            e.diagnosis = record_row[2]
            e.age = record_row[3]
            e.gender = record_row[4]
            m = sme.Measurement()
            m.time = record_row[5]
            m.ss = []
            c.execute("""
            SELECT signal
            FROM waveform
            WHERE (record_id = ?) and (edited = 0);""", (record_id, ))
            for signal_row in c.fetchall():
                s = sme.Signal()
                s.dt = 0.5
                s.x = np.array(np.frombuffer(signal_row[0]))
                m.ss.append(s)
            e.ms = [m]
            exams.append(e)
        conn.close()
        # try to join examinations
        joined_exams = exams
        # TODO
        return joined_exams
