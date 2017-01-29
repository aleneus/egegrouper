class GrouperController:
    def __init__(self, model, term_view):
        self.model = model
        self.term_view = term_view

    def db_info(self):
        info = self.model.db_info()
        self.term_view.db_info(info)

    def group_info(self, group_id):
        info = self.model.group_info(group_id)
        self.term_view.group_info(info)
