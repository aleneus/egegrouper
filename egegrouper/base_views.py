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

""" This module implements the base classes for views. """

class View:
    """ Base class for all views. """
    def show_data(self, data):
        """ Show data. 

        Parameters
        ----------
        data: Object
            Data to be shown.

        """
        raise NotImplementedError

class StatsView(View):
    """ Base class for stats views. """
    def __init__(self):
        """ Initialization. """
        self.title = None

    def show_data(self, data, headers):
        """ Show data. 

        Parameters
        ----------
        data : list of tuples
            Table data.
        headers : list of str
            Headers.

        """
        raise NotImplementedError
