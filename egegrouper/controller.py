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

"""
This module contains the Controller class.

The common scenario for controller is to ask connected model to make some data manipulation and then to ask suitable view to show data.

"""

from . import sme

class Controller:
    """Controller in MVC."""    

    def __init__(self, model):
        """Constructor. Set model.

        Parameters
        ----------
        model : egegrouper.GrouperModel
            Model.

        """
        self._model = model
        self._view_message = None
        self._view_storage = None
        self._view_group = None
        self._view_exam = None
        self._view_exam_plot = None
        self._view_where_exam = None

    def set_view_message(self, view):
        """Set view for show messages.

        Parameters
        ----------
        view
            View object.

        """
        self._view_message = view

    def set_view_storage(self, view):
        """Set view for show information about storage: groups, number of examinations in groups and number of ungrouped examination.

        Parameters
        ----------
        view
            View object.

        """
        self._view_storage = view
        
    def set_view_group(self, view):
        """Set view for show information about examinations in group.

        Parameters
        ----------
        view
            View object.

        """
        self._view_group = view
        
    def set_view_exam(self, view):
        """Set view for show information examination.

        Parameters
        ----------
        view
            View object.

        """
        self._view_exam = view
        
    def set_view_exam_plot(self, view):
        """Set view for plot signals of examination.

        Parameters
        ----------
        view
            View object.

        """
        self._view_exam_plot = view
        
    def set_view_where_exam(self, view):
        """Set view for show groups in which examination is.

        Parameters
        ----------
        view
            View object.

        """
        self._view_where_exam = view
        
    def show_message(self, text):
        """If controller has message view it asks view to show message.

        Parameters
        ----------
        text : str
            Text of message.

        """
        if not self._view_message:
            return
        self._view_message.show_data(text)

    def model_can_grumble(method):
        """Decorator. Try to do something and if model raises an exception return None.
        
        Parameters
        ----------
        method
            Method to decorate.

        """
        def wrapped(self, *args):
            try:
                return method(self, *args)
            except Exception as err:
                self.show_message('Something wrong') #TODO: more concrete messages
                #print(err.args) # uncomment for debugging
                return None
        wrapped.__doc__ = method.__doc__
        return wrapped

    @model_can_grumble
    def open_storage(self, file_name):
        """Open storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        file_name : str
            File name.

        """
        self._model.open_storage(file_name)
        self.storage_info()
        return True
        
    @model_can_grumble
    def create_storage(self, file_name):
        """Create storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        file_name : str
            File name.

        """
        self._model.create_storage(file_name)
        self.storage_info()
        return True

    @model_can_grumble
    def open_or_create_storage(self, file_name):
        """Open or create storage. Return True if success, None if an exception raised.

        If there are no data base it will be created.

        Parameters
        ----------
        file_name : str
            File name.

        """
        self._model.open_or_create_storage(file_name)
        self.storage_info()
        return True

    @model_can_grumble
    def close_storage(self):
        """Close storage. Return True if success, None if an exception raised."""
        self._model.close_storage()

    @model_can_grumble
    def storage_info(self):
        """Show common information about storage. Return True if success, None if an exception raised."""
        data, headers = self._model.storage_info()
        self._view_storage.show_data(data, headers)
        return True

    @model_can_grumble
    def group_info(self, group_id):
        """Show list of examinations of group. Return True if success, None if an exception raised.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        data, headers = self._model.group_info(group_id)
        self._view_group.show_data(data, headers)
        return True

    @model_can_grumble
    def exam(self, exam_id):
        """Show information about selected examination. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self._model.exam(exam_id)
        if e == None:
            self.show_message('Exam data is empty.')
            return True
        self._view_exam.show_data(e)
        return True

    @model_can_grumble
    def plot_exam(self, exam_id):
        """Plot signals of examination. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self._model.exam(exam_id)
        if e == None:
            self.show_message('Exam data is empty.')
            return True
        self._view_exam_plot.show_data(e)
        return True

    @model_can_grumble
    def insert_group(self, name, description):
        """Add new group to current storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        name : str
            Name of new group.
        description : str
            Description of new group.

        """
        self._model.insert_group(name, description)
        self.storage_info()
        return True

    @model_can_grumble
    def delete_group(self, group_id):
        """Delete group. Return True if success, None if an exception raised.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        self._model.delete_group(group_id)
        self.storage_info()
        return True

    @model_can_grumble
    def group_exam(self, exam_id, group_ids, placed_in):
        """Add and delete examination to and from groups. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            Examination identifier.
        group_ids : list of str
            Group identifiers.
        placed_in : list of bool
            True for examinations to be placed in groups. Length of group_ids must be equal to length of placed_in.

        """
        self._model.group_exam(exam_id, group_ids, placed_in)
        return True

    @model_can_grumble
    def where_exam(self, exam_id):
        """Show information of groups where examination is. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        group_records, headers, placed_in = self._model.where_exam(exam_id)
        self._view_where_exam.show_data(group_records, headers, placed_in)
        return True

    @model_can_grumble
    def add_sme_db(self, file_name):
        """Add SME sqlite3 data base to current storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        file_name : str
            File name. Example: example.sme.sqlite.

        """
        self._model.add_sme_db(file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def add_gs_db(self, file_name):
        """Add GS sqlite3 data base to current storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        file_name : str
            File name. Example: example.gs.sqlite.

        """
        self._model.add_gs_db(file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def add_exam_from_json_file(self, file_name):
        """Add examination from JSON file to current storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        file_name : str
            Name of JSON file.
        
        """
        self._model.add_exam_from_json_file(file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def export_exam_to_json_file(self, exam_id, file_name):
        """Export examination to JSON file. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        file_name : str
            Name of JSON file.

        """
        self._model.export_exam_to_json_file(exam_id, file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def delete_exam(self, exam_id):
        """Delete examination from storage. Return True if success, None if an exception raised.

        Parameters
        ----------
        exam_id : str
            ID of examination to be deleted.
        
        """
        self._model.delete_exam(exam_id)
        return True

    @model_can_grumble
    def merge_exams(self, exam_id_1, exam_id_2):
        """Merge two exams. Return True if success, None if an exception raised.
        
        Create joined examination and put it to storage. Add measurements from examination 2 to examination 1.

        Parameters
        ----------
        exam_id_1 : str
            Examination 1 ID.
        exam_id_2 : str
            Examination 2 ID.

        """
        e1 = self._model.exam(exam_id_1)
        e2 = self._model.exam(exam_id_2)
        e = sme.merge_exams(e1, e2)
        self._model.insert_exam(e)
        self.show_message('Done')
        return True

    @model_can_grumble
    def group_record(self, group_id):
        """Return group record.

        Parameters
        ----------
        group_id : str
            Group ID.

        Return
        ------
        : OrderedDict
            Attributes names and values. If an exception raised return None.

        """
        return self._model.group_record(group_id)

    @model_can_grumble
    def update_group_record(self, group_id, attr):
        """ Update attribute values of selected group. Return True if success, None if an exception raised.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        """
        self._model.update_group_record(group_id, attr)
        return True
