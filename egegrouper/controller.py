import os.path # TODO: remove from here (?)
from egegrouper import sme

class GrouperController:
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

    def set_model(self, model):
        """Set model.

        Parameters
        ----------
        model : egegrouper.GrouperModel
            Model.

        """
        self.model = model

    def open_or_create_storage(self, file_name):
        """Open or create storage.

        If there are no data base it will be created.

        Parameters
        ----------
        file_name : str
            File name.

        """
        if os.path.isfile(file_name):
            self.model.open_storage(file_name)
        else:
            self.model.create_storage(file_name)

    def close_storage(self):
        """Close storage."""
        self.model.close_storage()

    def storage_info_new(self):
        """Show common information about storage."""
        data, headers = self.model.storage_info_new()
        self.view_storage.set_data([data, headers])
        self.view_storage.show_data()
        
    def group_info(self, group_id):
        """Show list of examinations of group.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        rows, headers = self.model.group_info(group_id)
        self.view_group.set_data([rows, headers])
        self.view_group.show_data()

    def exam(self, exam_id):
        """Show information about selected examination.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self.model.get_examination(exam_id)
        if not e:
            self.view_message.set_data('Something wrong')
            self.view_message.show_data()
            return
        self.view_exam.set_data(e)
        self.view_exam.show_data()

    def plot_exam(self, exam_id):
        """Plot signals of examination.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self.model.get_examination(exam_id)
        if not e:
            self.view_message.set_data('Something wrong')
            self.view_message.show_data()
            return
        self.view_exam_plot.set_data(e)
        self.view_exam_plot.show_data()  

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
        self.storage_info_new()

    def delete_group(self, group_id):
        """Delete group.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        self.model.delete_group(group_id)
        self.storage_info_new()

    def add_exam_to_group(self, exam_id, group_id):
        """Add examination to group.

        Parameters
        ----------
        exam_id : str
            Examintion ID.
        group_id : str
            Group ID.

        """
        self.model.add_exam_to_group(exam_id, group_id)

    def delete_exam_from_group(self, exam_id, group_id):
        """Delete examination from group.

        Parameters
        ----------
        exam_id : str
            Examintion ID.
        group_id : str
            Group ID.

        """
        self.model.delete_exam_from_group(exam_id, group_id)

    def where_is_examination(self, exam_id):
        """Show information of groups where examination is.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        data = self.model.where_is_examination(exam_id)
        self.view_where_exam.set_data([data, ("Group ID", "Group name")])
        self.view_where_exam.show_data()
        
    def add_sme_db(self, file_name):
        """Add SME sqlite3 data base to current storage.

        Parameters
        ----------
        file_name : str
            File name. Example: example.sme.sqlite.

        """
        self.model.add_sme_db(file_name)

    def add_gs_db(self, file_name):
        """Add GS sqlite3 data base to current storage.

        Parameters
        ----------
        file_name : str
            File name. Example: example.gs.sqlite.

        """
        self.model.add_gs_db(file_name)

    def add_exam_from_json_folder(self, folder_name):
        """Add examination from JSON folder to current storage.

        Parameters
        ----------
        folder_name : str
            Name of folder wich should contain the file info.json.
        
        """
        if not self.model.add_exam_from_json_folder(folder_name):
            self.view_message.set_data('Something wrong.')
        self.view_message.set_data('Done.')
        self.view_message.show_data()

    def export_as_json_folder(self, exam_id, folder_name):
        """Export examination to JSON folder.

        Parameters
        ----------
        exam_id : str
            Examination ID.
        folder_name : str
            Name of folder for export info.json and signals in text format.

        """
        if self.model.export_as_json_folder(exam_id, folder_name):
            self.view_message.set_data('Done.')
        else:
            self.view_message.set_data('Something wrong.')
        self.view_message.show_data()

    def delete_exam(self, exam_id):
        """Delete examination from storage.

        Parameters
        ----------
        exam_id : str
            ID of examination to be deleted.
        
        """
        self.model.delete_exam(exam_id)

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
        e1 = self.model.get_examination(exam_id_1)
        e2 = self.model.get_examination(exam_id_2)
        e = sme.merge_exams(e1, e2)
        self.model.insert_examination(e)
        # todo exceptions
        self.view_message.set_data('Done')
        self.view_message.show_data()

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

    def update_group_record(self, group_id, attr):
        """ Update attribute values of selected group.

        Parameters
        ----------
        group_id : str
            Group ID.
        attr : OrderedDict
            Attributes names and values.

        Return
        ------
        : str
        
        """
        self.model.update_group_record(group_id, attr)
        # TODO exceptions
        self.view_message.set_data('Done')
        self.view_message.show_data()
