class GrouperModel:
    def __init__(self):
        pass

    """ Work with DB
    """

    def create_db(self, fname):
        pass

    def open_db(self, file_name):
        pass

    def close_db(self):
        pass

    def db_opened(self):
        pass
    
    """ Mapping
    """
    
    def get_examination(self, exam_id):
        pass

    def insert_examination(self, e):
        pass

    """ Data Viewing
    """

    def db_info(self):
        pass

    def group_info(self, group_id):
        pass

    """ Grouping
    """
    
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

    """ Import and export
    """

    def add_sme_db(self, fname):
        pass

    def add_gs_db(self, fname):
        pass

    def add_exam_from_json_folder(self, folder_name):
        pass

    def export_as_json_folder(self, exam_id, folder_name):
        pass

    """ Other data manipulation
    """

    def delete_exam(self, exam_id):
        pass
    
