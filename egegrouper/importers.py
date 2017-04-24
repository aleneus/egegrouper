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
        self.controller.add_exams_to_storage(es)

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
    """TODO doc it
    
    """
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
        print("Start import GS database...")
        return []

# Think about split it to files. Separate file for every importer.
