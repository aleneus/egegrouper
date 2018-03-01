""" Controller for connection of user, StatsModel and views. """

class StatsController:
    def __init__(self):
        self.model = None
        self.view = None
    
    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        # TODO: it is stub
        self.view = view

    def gender_balance(self, group_id):
        data = self.model.gender_balance(group_id)
        self.view.show_data(data)

    def aver_age(self, group_id):
        value = self.model.aver_age(group_id)
        self.view.show_data(value)
