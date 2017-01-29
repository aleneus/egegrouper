class GrouperController:
    def __init__(self, model, term_view, plot_view):
        self.model = model
        self.term_view = term_view
        self.plot_view = plot_view

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
            self.plot_view.plot_examination(e)
