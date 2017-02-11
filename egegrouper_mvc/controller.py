import os.path

class GrouperController:
    def __init__(self, model = None, view = None):
        self.model = model
        self.view = view

    def set_model(self, model):
        self.model = model
        self.view = view

    def set_view(self, view):
        self.view = view
        
    def open_or_create_db(self, fname):
        if os.path.isfile(fname):
            self.model.open_db(fname)
        else:
            self.model.create_db(fname)

    def close_db(self):
        self.model.close_db()

    def db_info(self):
        data = self.model.db_info()
        return self.view.db(data)

    def group_info(self, group_id):
        data = self.model.group_info(group_id)
        return self.view.table(data)

    def exam_info(self, exam_id):
        info = self.model.exam_info(exam_id)
        if not info:
            return self.view.error_message('Something wrong')
        return self.view.exam(info)

    def plot_exam(self, exam_id):
        e = self.model.get_examination(exam_id)
        if not e:
            return self.view.error_message('Something wrong')
        return self.view.exam(e)
        
    def insert_group(self, name, description):
        self.model.insert_group(name, description)
        return self.db_info()

    def delete_group(self, group_id):
        self.model.delete_group(group_id)
        return self.db_info()

    def add_exam_to_group(self, exam_id, group_id):
        self.model.add_exam_to_group(exam_id, group_id)

    def delete_exam_from_group(self, exam_id, group_id):
        self.model.delete_exam_from_group(exam_id, group_id)

    def where_is_examination(self, exam_id):
        data = self.model.where_is_examination(exam_id)
        return self.view.table(data)
        
    def add_sme_db(self, fname):
        self.model.add_sme_db(fname)

    def add_gs_db(self, fname):
        self.model.add_gs_db(fname)

    def add_exam_from_json_folder(self, folder_name):
        if not self.model.add_exam_from_json_folder(folder_name):
            return self.view.error_message('Something wrong')
        return self.view.message('Done')

    def export_as_json_folder(self, exam_id, folder_name):
        self.model.export_as_json_folder(exam_id, folder_name)

    def delete_exam(self, exam_id):
        self.model.delete_exam(exam_id)
