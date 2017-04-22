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
        
        Returns
        -------
        bool
            True if success, False if not.

        """
        es = self._get_exams(source)
        self.controller.add_exams(es)
        return True # TODO

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
    
class GSImporter(BaseImporter):
    def _get_exams(self, source):
        return []
