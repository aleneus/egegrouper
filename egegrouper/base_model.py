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

class BaseModel(ABC):
    """Model in MVC. Base class."""
    
    def __init__(self):
        """Constructor.
        
        Create fields and set initial state of model.
        
        """
        self._state = {}

    def set_state(self, **kwargs):
        """Set model state."""
        for key in kwargs:
            self._state[key] = kwargs[key]

    def state(self):
        """Return model state."""
        return self._state

    @staticmethod
    def do_if_storage_opened(method):
        """Decorator. If storage is not opened AttributeError raised."""
        def wrapped(self, *args):
            if not self.state()['storage_opened']:
                raise AttributeError('Storage is not opened.')
            return method(self, *args)
        wrapped.__doc__ = method.__doc__
        return wrapped

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

    @abstractmethod
    def create_storage(self, name):
        """Create new storage.

        Parameters
        ----------
        name : str
            Storage name.

        """
        pass

    @abstractmethod
    def open_storage(self, name):
        """Open storage.

        Parameters
        ----------
        name : str
            Storage name.

        """
        pass

    @abstractmethod
    def close_storage(self):
        """Close current storage."""
        pass

    @abstractmethod
    def storage_exists(self, name):
        """Check if the storage exists.

        Parameters
        ----------
        name : str
            Name of storage.

        Returns
        -------
        : bool
            True if exists, False otherwise.

        """
        pass

    @abstractmethod
    def exam(self, exam_id):
        """Return examination object.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        Returns
        -------
        sme.Examination
            Examination object.

        """
        pass

    @abstractmethod
    def insert_exam(self, exam):
        """Add examination into current storage.

        Parameters
        ----------
        exam : sme.Examination
            Examination object

        """
        pass

    @abstractmethod
    def delete_exam(self, exam_id):
        """Delete examination from current storage.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        pass
    
    @abstractmethod
    def storage_info(self):
        """Return common information about current storage.

        Return
        ------
        data : list of tuples
            Table with information about storage.
        headers : tuple
            Headers.

        """
        pass

    @abstractmethod
    def group_info(self, group_id):
        """Return information about examinations of selected group.

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
        pass

    @abstractmethod
    def insert_group(self, name, description):
        """Add new group of examinations.

        Parameters
        ----------
        name : str
            Name of new group.
        description : str
            Description for new group.

        """
        pass

    @abstractmethod
    def delete_group(self, group_id):
        """Delete group of examinations from storage.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def update_group_record(self, group_id, attr):
        """Update group record in storage.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        """
        pass
