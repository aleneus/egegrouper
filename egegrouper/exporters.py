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

from . import sme_json
import os

class BaseExporter:
    """Base class for exporters."""

    def export_exam(self, exam, dest_name):
        """ Export examination to destination with dest_name.

        Parameters
        ----------
        exam : sme.Examination
            Examination instance.
        dest_name : str
            Destination name.

        """
        pass

class JsonFileExporter(BaseExporter):
    """Exporter to JSON file."""

    def export_exam(self, exam, dest_name):
        """ Export examination to JSON file with dest_name.

        Parameters
        ----------
        exam : sme.Examination
            Examination instance.
        dest_name : str
            JSON file name.

        """
        abs_file_name = os.path.expanduser(dest_name)
        sme_json.put_exam(exam, abs_file_name)
