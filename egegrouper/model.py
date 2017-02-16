from egegrouper.sme import *
from egegrouper.db_import import *
from egegrouper.sme_json_folders import *

class GrouperModel():
    """Model in MVC. Base class."""
    def __init__(self):
        pass

    # Work with storage

    def create_storage(self, name):
        """Create new storage."""
        pass

    def open_storage(self, name):
        """Open an existing storage."""
        pass

    def close_storage(self):
        """Close current storage."""
        pass

    def storage_opened(self):
        """Check if storage is opened."""
        pass
    
    # Mapping
    
    def get_examination(self, exam_id):
        """Return examination."""
        pass

    def insert_examination(self, e):
        """Add examination into current storage."""
        pass

    # Data Viewing

    def storage_info(self):
        """Return storage info."""
        pass

    def group_info(self, group_id):
        """Return group info."""
        pass

    # Grouping
    
    def insert_group(self, name, description):
        """Add new group to current storage."""
        pass

    def delete_group(self, group_id):
        """Delete group."""
        pass

    def add_exam_to_group(self, exam_id, group_id):
        """Add examination to group."""
        pass

    def delete_exam_from_group(self, exam_id, group_id):
        """Delete examination from group."""
        pass

    def where_is_examination(self, exam_id):
        """Return description of groups where examination is."""
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
    
