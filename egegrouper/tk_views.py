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

import tkinter as tk
from tkinter import ttk, messagebox

from .base_views import View, StatsView

class MessageTkView(View):
    """Text message view."""
    def show_data(self, text):
        """ Show message box.

        Parameters
        ----------
        text : str
            Message text.

        """
        messagebox.showinfo("Message", text)

class StorageTkView(View):
    """ View for showing information about storage. """
    def __init__(self):
        self._widget = None

    def get_widget(self):
        return self._widget
    def set_widget(self, widget):
        headers = ["ID", "Name", "Description", "Num"]
        widths = [50, None, None, 50]
        anchors = [tk.CENTER, None, None, tk.CENTER]
        widget.set_columns(headers=headers, widths=widths, anchors=anchors)
        self._widget = widget
    widget = property(get_widget, set_widget, doc="Table widget")

    def show_data(self, data, headers):
        self.widget.update_data(data)

class GroupTkView(View):
    """ View for showing information about group. """
    def __init__(self):
        self._widget = None

    def get_widget(self):
        return self._widget
    def set_widget(self, widget):
        headers = ["ID", "Name", "Diagnosis", "Age", "Gender"]
        widths = [50, None, None, None, None]
        anchors = [None, None, None, tk.CENTER, tk.CENTER]
        widget.set_columns(headers=headers, widths=widths, anchors=anchors)
        self._widget = widget
    widget = property(get_widget, set_widget, doc="Table widget")

    def show_data(self, data, headers):
        self.widget.update_data(data)

class StatsTkView(StatsView):
    def __init__(self, parent):
        """ Initialization. """
        super().__init__()
        self.parent = parent

    def show_data(self, data, headers):
        """ Show data. 

        Parameters
        ----------

        data: list of lists
            Table content.
        headers: list of str
            Headers.
        """
        table = self._build_window(self.parent)
        table.update_data(data)

    def _build_window(self, parent):
        """ Build and show window with table inside. """
        master = tk.Toplevel(parent)
        if self.title is not None:
            master.title(self.title)
        else:
            master.title("Statistics")
        table = TableWidget(master) 
        table.set_columns(
            headers=['Category', 'Number'],
            widths=[None, None],
            anchors=[None, tk.CENTER],
        )
        table.pack()
        master.transient(parent)
        return table

class WhereExamTkView(View):
    """ View showing in which groups the exam is located. """
    def __init__(self):
        self._widget = None
 
    def get_widget(self):
        return self._widget
    def set_widget(self, widget):
        self._widget = widget
    widget = property(get_widget, set_widget, doc="Grouping table widget")
    
    def show_data(self, group_records, headers, placed_in):
        rows = [
            (gr[0], gr[1], 'X' if p else '')
            for p, gr in zip(placed_in, group_records)
        ]
        headers_ext = headers + ('', )
        self.widget.update_data(rows)
