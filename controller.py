import os.path

class GrouperController:
    def __init__(self, model, term_view, plot_view):
        self.model = model
        self.term_view = term_view
        self.plot_view = plot_view

    def open_or_create_db(self, fname):
        if os.path.isfile(fname):
            self.model.open_db(fname)
            self.term_view.message('{} was opened'.format(fname))
        else:
            self.model.create_db(fname)
            self.term_view.message('{} was created'.format(fname))

    def close_db(self):
        self.model.close_db()

    def db_info(self):
        info = self.model.db_info()
        self.term_view.db_info(info)

    def group_info(self, group_id):
        info = self.model.group_info(group_id)
        self.term_view.group_info(info)

    def exam_info(self, exam_id, ofile = None):
        info = self.model.exam_info(exam_id)
        self.term_view.exam_info(info)
        if ofile:
            e = self.model.get_examination(exam_id)
            self.plot_view.plot_examination(e, ofile)

    def insert_group(self, name, description):
        self.model.insert_group(name, description)
        self.db_info()

    def delete_group(self, group_id):
        answer = input('Are your shure? Type yes or no: ')
        if answer == 'yes':
            self.model.delete_group(group_id)
            self.db_info()

    def add_to_group(self, exam_id, group_id):
        self.model.add_to_group(exam_id, group_id)

    def delete_from_group(self, exam_id, group_id):
        self.model.delete_from_group(exam_id, group_id)

    def add_data_from_sme(self, fname):
        self.model.add_data_from_sme(fname)
