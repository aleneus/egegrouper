class GrouperController:
    def __init__(self, model, term_view):
        self.model = model
        self.term_view = term_view

    def db_info(self):
        info = self.model.db_info()
        self.term_view.db_info(info)
