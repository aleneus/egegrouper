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
    
    model = None
    """Model."""
    
    view_message = None
    """View for messages."""

    view_storage = None
    """View for common information about storage."""

    view_group = None
    """View for information about examination in group."""
    
    view_exam = None
    """View for details of one examination."""

    view_exam_plot = None
    """View for plotting signals of examination."""

    view_where_exam = None
    """View for groups in which the examination is."""

    def __init__(self, model):
        """Set model.

        Parameters
        ----------
        model : egegrouper.GrouperModel
            Model.

        """
        self.model = model

    def show_message(self, text):
        """If controller has message view it asks veiw to show message."""
        if not self.view_message:
            return
        self.view_message.show_data(text)

    def model_can_grumble(method):
        """Decorator. Try to do something and if model raises an exception return None."""
        def wrapped(self, *args):
            try:
                return method(self, *args)
            except Exception:
                self.show_message('Something wrong') #TODO: more concrete messages
                return None
        wrapped.__doc__ = method.__doc__
        return wrapped

    @model_can_grumble
    def open_storage(self, file_name):
        """Open storage.

        Parameters
        ----------
        file_name : str
            File name.

        """
        self.model.open_storage(file_name)
        self.storage_info()
        return True
        
    @model_can_grumble
    def create_storage(self, file_name):
        """Create storage.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if not self.model.create_storage(file_name):
            return False
        self.storage_info()
        return True

    @model_can_grumble
    def open_or_create_storage(self, file_name):
        """Open or create storage.

        If there are no data base it will be created.

        Parameters
        ----------
        file_name : str
            File name.

        """
        self.model.open_or_create_storage(file_name)
        self.storage_info()
        return True

    @model_can_grumble
    def close_storage(self):
        """Close storage."""
        self.model.close_storage()

    @model_can_grumble
    def storage_info(self):
        """Show common information about storage."""
        data, headers = self.model.storage_info()
        self.view_storage.show_data(data, headers)
        return True

    @model_can_grumble
    def group_info(self, group_id):
        """Show list of examinations of group.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        data, headers = self.model.group_info(group_id)
        self.view_group.show_data(data, headers)
        return True

    @model_can_grumble
    def exam(self, exam_id):
        """Show information about selected examination.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self.model.exam(exam_id)
        if e == None:
            self.show_message('Exam data is empty.')
            return True
        self.view_exam.show_data(e)
        return True

    @model_can_grumble
    def plot_exam(self, exam_id):
        """Plot signals of examination.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self.model.exam(exam_id)
        if e == None:
            self.show_message('Exam data is empty.')
            return True
        self.view_exam_plot.show_data(e)
        return True

    @model_can_grumble
    def insert_group(self, name, description):
        """Add new group to current storage.

        Parameters
        ----------
        name : str
            Name of new group.
        description : str
            Description of new group.

        """
        self.model.insert_group(name, description)
        self.storage_info()
        return True

    @model_can_grumble
    def delete_group(self, group_id):
        """Delete group.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        self.model.delete_group(group_id)
        self.storage_info()
        return True

    @model_can_grumble
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
        self.model.group_exam(exam_id, group_ids, placed_in)
        return True

    @model_can_grumble
    def where_exam(self, exam_id):
        """Show information of groups where examination is.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        group_records, headers, placed_in = self.model.where_exam(exam_id)
        self.view_where_exam.show_data(group_records, headers, placed_in)
        return True

    @model_can_grumble
    def add_sme_db(self, file_name):
        """Add SME sqlite3 data base to current storage.

        Parameters
        ----------
        file_name : str
            File name. Example: example.sme.sqlite.

        """
        self.model.add_sme_db(file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def add_gs_db(self, file_name):
        """Add GS sqlite3 data base to current storage.

        Parameters
        ----------
        file_name : str
            File name. Example: example.gs.sqlite.

        """
        self.model.add_gs_db(file_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def add_exam_from_json_folder(self, folder_name):
        """Add examination from JSON folder to current storage.

        Parameters
        ----------
        folder_name : str
            Name of folder wich should contain the file info.json.
        
        """
        self.model.add_exam_from_json_folder(folder_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def export_as_json_folder(self, exam_id, folder_name):
        """Export examination to JSON folder.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        folder_name : str
            Name of folder for export info.json and signals in text format.

        """
        self.model.export_as_json_folder(exam_id, folder_name)
        self.show_message('Done.')
        return True

    @model_can_grumble
    def delete_exam(self, exam_id):
        """Delete examination from storage.

        Parameters
        ----------
        exam_id : str
            ID of examination to be deleted.
        
        """
        self.model.delete_exam(exam_id)
        return True

    @model_can_grumble
    def merge_exams(self, exam_id_1, exam_id_2):
        """Merge two exams.
        
        Create joined examination and put it to storage. Add measuremets from examination 2 to examination 1.

        Parameters
        ----------
        exam_id_1 : str
            Examination 1 ID.
        exam_id_2 : str
            Examination 2 ID.

        """
        e1 = self.model.exam(exam_id_1)
        e2 = self.model.exam(exam_id_2)
        e = sme.merge_exams(e1, e2)
        self.model.insert_exam(e)
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
            Attributes names and values.

        """
        return self.model.group_record(group_id)

    @model_can_grumble
    def update_group_record(self, group_id, attr):
        """ Update attribute values of selected group.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        """
        self.model.update_group_record(group_id, attr)
        return True
