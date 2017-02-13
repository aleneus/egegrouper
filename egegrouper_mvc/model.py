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

    """ Other data manipulation
    """

    def delete_exam(self, exam_id):
        pass
    
