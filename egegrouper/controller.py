import os.path
from egegrouper import sme

class GrouperController:
    """Controller in MVC.

    Asks model to do something with storage and then asks view to represent data and return answer from view.

    """
    
    def __init__(self, model = None, view = None):
        """Set model and view.

        Parameters
        ----------
        model : egegrouper.GrouperModel
        view : egegrouper.View

        """
        self.model = model
        self.view = view

    def set_model(self, model):
        """Set model.

        Parameters
        ----------
        model : egegrouper.GrouperModel
            Model.

        """
        self.model = model
        self.view = view

    def set_view(self, view):
        """Set view.

        Different views may be needed.

        Parameters
        ----------
        view : egegrouper.View
            View.

        """
        self.view = view
        
    def open_or_create_storage(self, file_name):
        """Open or create data base.

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

    def storage_info(self):
        """Return storage info."""
        exams_num, data, num_in_groups, ungrouped_num = self.model.storage_info()
        return self.view.storage(exams_num, data, num_in_groups, ungrouped_num)

    def group_info(self, group_id):
        """Return group info.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        d, h = self.model.group_info(group_id)
        return self.view.table(d, headers = h)

    def exam(self, exam_id):
        """Return examination info.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        e = self.model.get_examination(exam_id)
        if not e:
            return self.view.error_message('Something wrong')
        return self.view.exam(e)

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
        return self.storage_info()

    def delete_group(self, group_id):
        """Delete group.

        Parameters
        ----------
        group_id : str
            Group ID.

        """
        self.model.delete_group(group_id)
        return self.storage_info()

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
        """Return information of groups where examination is.

        Parameters
        ----------
        exam_id : str
            Examination ID.

        """
        data = self.model.where_is_examination(exam_id)
        return self.view.table(data)
        
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
            return self.view.error_message('Something wrong')
        return self.view.message('Done')

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
        return self.view.message('Done')
