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

class GrouperModel():
    """Model in MVC. Base class."""
    
    def __init__(self):
        self._state = {}
        self._state['storage_opened'] = False
        self._state['file_name'] = None

    # Common work with storage

    def create_storage(self, name):
        """Create new storage."""
        pass

    def open_storage(self, name):
        """Open an existing storage."""
        pass

    def close_storage(self):
        """Close current storage."""
        pass

    def storage_exists(self, name):
        """Check if storage exists.

        Returns
        -------
        : bool
            True if exists, False overwise.

        """
        pass

    def open_or_create_storage(self, name):
        """Open or create storage (if stoarge not exists).
        
        Parameters
        ----------
        name : str
            Name of storage.
        
        """
        if self.storage_exists(name):
            self.open_storage(name)
        else:
            self.create_storage(name)

    # Model state

    def set_state(self, key, value):
        """Set model state."""
        self._state[key] = value

    def state(self):
        """Return model state."""
        return self._state

    # Mapping
    
    def get_examination(self, exam_id):
        """Return examination."""
        pass

    def insert_examination(self, e):
        """Add examination into current storage."""
        pass


    # Data Viewing

    def storage_info(self):
        """Return common information about current storage."""
        pass

    def group_info(self, group_id):
        """Return short information about examinations of selected group."""
        pass


    # Grouping
    
    def insert_group(self, name, description):
        """Add new group to current storage."""
        pass

    def delete_group(self, group_id):
        """Delete group."""
        pass

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
        pass

    def where_exam(self, exam_id):
        """Return description of groups where examination in or not in."""
        pass


    # Import and export

    def add_sme_db(self, file_name):
        """Add records from SME storage to current storage."""
        pass

    def add_gs_db(self, file_name):
        """Add records from Gastroscan sqlite3 data base to current storage."""
        pass

    def add_exam_from_json_folder(self, folder_name):
        """Add examination fron JSON folder to current storage."""
        pass

    def export_as_json_folder(self, exam_id, folder_name):
        """Export examination fo JSON folder."""
        pass


    # Other data manipulation

    def delete_exam(self, exam_id):
        """Delete examination from storage."""
        pass
