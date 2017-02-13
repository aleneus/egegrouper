from egegrouper_mvc.sme import *
from egegrouper_mvc.db_import import *
from egegrouper_mvc.sme_json_folders import *

class GrouperModel:
    def __init__(self):
        pass

    # Work with storage

    def create_storage(self, name):
        pass

    def open_storage(self, name):
        pass

    def close_storage(self):
        pass

    def storage_opened(self):
        pass
    
    # Mapping
    
    def get_examination(self, exam_id):
        pass

    def insert_examination(self, e):
        pass

    # Data Viewing

    def storage_info(self):
        pass

    def group_info(self, group_id):
        pass

    # Grouping
    
    def insert_group(self, name, description):
        pass

    def delete_group(self, group_id):
        pass

    def add_exam_to_group(self, exam_id, group_id):
        pass

    def delete_exam_from_group(self, exam_id, group_id):
        pass

    def where_is_examination(self, exam_id):
        pass

    # Import and export

    def add_sme_db(self, file_name):
        pass

    def add_gs_db(self, file_name):
        pass

    def add_exam_from_json_folder(self, folder_name):
        pass

    def export_as_json_folder(self, exam_id, folder_name):
        pass


    # Other data manipulation

    def delete_exam(self, exam_id):
        pass
    
