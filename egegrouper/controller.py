import os.path
from egegrouper import sme

class GrouperController:
    """Controller in MVC.

    Asks model to do something with storage and then asks view to represent data.

    """
    
    def __init__(self, model = None, view = None):
        """Set model and view to work with."""
        self.model = model
        self.view = view

    def set_model(self, model):
        """Set model."""
        self.model = model
        self.view = view

    def set_view(self, view):
        """Set view.

        Different views may be needed."""
        self.view = view
        
    def open_or_create_storage(self, fname):
        """Open or create data base.

        If there are no data base it will be created."""
        if os.path.isfile(fname):
            self.model.open_storage(fname)
        else:
            self.model.create_storage(fname)

    def close_storage(self):
        """Close storage."""
        self.model.close_storage()

    def storage_info(self):
        """Get and pass storage info."""
        data = self.model.storage_info()
        return self.view.storage(data)

    def group_info(self, group_id):
        """Get and pass group info."""
        d, h = self.model.group_info(group_id)
        return self.view.table(d, headers = h)

    def exam(self, exam_id):
        """Get and pass examination info."""
        e = self.model.get_examination(exam_id)
        if not e:
            return self.view.error_message('Something wrong')
        return self.view.exam(e)

    def insert_group(self, name, description):
        """Add new group."""
        self.model.insert_group(name, description)
        return self.storage_info()

    def delete_group(self, group_id):
        """Delete group."""
        self.model.delete_group(group_id)
        return self.storage_info()

    def add_exam_to_group(self, exam_id, group_id):
        """Add examination to group."""
        self.model.add_exam_to_group(exam_id, group_id)

    def delete_exam_from_group(self, exam_id, group_id):
        """Delete examination from group."""
        self.model.delete_exam_from_group(exam_id, group_id)

    def where_is_examination(self, exam_id):
        """Return information of groups where examination is."""
        data = self.model.where_is_examination(exam_id)
        return self.view.table(data)
        
    def add_sme_db(self, fname):
        """Add SME sqlite3 data base to current storage."""
        self.model.add_sme_db(fname)

    def add_gs_db(self, fname):
        """Add GS sqlite3 data base to current storage."""
        self.model.add_gs_db(fname)

    def add_exam_from_json_folder(self, folder_name):
        """Add examination from JSON folder to current storage."""
        if not self.model.add_exam_from_json_folder(folder_name):
            return self.view.error_message('Something wrong')
        return self.view.message('Done')

    def export_as_json_folder(self, exam_id, folder_name):
        """Export examination to JSON folder."""
        self.model.export_as_json_folder(exam_id, folder_name)

    def delete_exam(self, exam_id):
        """Delete examination from storage."""
        self.model.delete_exam(exam_id)

    def merge_exams(self, exam_id_1, exam_id_2):
        """Merge two exams.
        
        Create joined examination and put it to storage.
        """
        e1 = self.model.get_examination(exam_id_1)
        e2 = self.model.get_examination(exam_id_2)
        e = sme.merge_exams(e1, e2)
        self.model.insert_examination(e)
        return self.view.message('Done')
