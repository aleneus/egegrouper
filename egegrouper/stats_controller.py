# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Controller for connection of user, StatsModel and views. """

class StatsController:
    def __init__(self):
        self.model = None
        self.view = None
        self.status_view = None
        self.table_view = None
        self.message_view = None

    def stats(self, key, group_id):
        # TODO: check if some view is None
        self.status_view.show_data("Calculating stats...")
        data = self.model.stats(key, group_id)
        if len(data) == 0:
            self.message_view.show_data("Result is empty")
            return
        table_data = [[key, data[key]] for key in data]
        self.table_view.show_data(table_data)
    
    def gender_balance(self, group_id):
        data = self.model.gender_balance(group_id)
        self.view.show_data(data)

    def aver_age(self, group_id):
        value = self.model.aver_age(group_id)
        self.view.show_data(value)
