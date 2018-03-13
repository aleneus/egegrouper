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

""" Custom widgets based on tkinter. """

import tkinter as tk
from tkinter import ttk, messagebox

from .simple_signal import SimpleSignal

class TableWidget(tk.Frame):
    """ Table widget. """
    def __init__(self, parent, headers = []):
        """ Constructor.

        Parameters
        ----------
        parent
            Master for widget.
        headers : list of str
            Headers for table.

        """
        tk.Frame.__init__(self, parent)
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.set_columns(headers=headers)
        # signals
        self.item_opened = SimpleSignal()
        self.tree.bind("<Double-1>", self.item_opened.emit)
        self.tree.bind("<Return>", self.item_opened.emit)
        self.item_selected = SimpleSignal()
        self.tree.bind("<<TreeviewSelect>>", self.item_selected.emit)
        
    def selected_item_text(self):
        """ Return text in selected item.

        Returns
        -------
        item_text : str.
            Text of selected item.
        
        """
        try:
            item = self.tree.selection()[0]
            item_text = self.tree.item(item,"text")
        except IndexError:
            item_text = None
        finally:
            return item_text

    def set_columns(self, headers=[], anchors=[], widths=[]):
        """ Setup columns.

        Parameters
        ----------
        headers : list of str
            Headers for table.
        anchors : list of str
            Anchors for columns. Use for align content.
        widths : list of int
            Widths of columns.

        """
        if len(headers) > 0:
            self.column_ids = ["#0",] + headers[1:]
            self.tree["columns"] = headers[1:]
            for (cid, h) in zip(self.column_ids, headers):
                self.tree.heading(cid, text=h)
        if len(anchors) > 0:
            for (cid, a) in zip(self.column_ids, anchors):
                self.tree.column(cid, anchor=a)
        if len(widths) > 0:
            for (cid, w) in zip(self.column_ids, widths):
                self.tree.column(cid, width=w)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def update_data(self, data):
        """ Fill table with data.

        Parameters
        ----------
        data : list of tuple of str
            Data in table rows.
        
        """
        self.clear()
        for (i, row) in zip(range(len(data)), data):
            self.tree.insert("", tk.END, iid = str(i), text=str(row[0]), values=row[1:])
        
    def clear(self):
        """ Clear all items. """
        self.tree.delete(*self.tree.get_children())

    def remember_selection(self):
        """ Remember selected item. """
        self._selected_item = self.tree.selection()[0]
        
    def restore_selection(self):
        """ Restore selection. """
        if not self.tree.exists(self._selected_item):
            return
        self.tree.selection_set(self._selected_item)
        
class GroupingTable(TableWidget):
    """ Table widget for grouping. """
    def __init__(self, parent):
        """ Constructor.

        Parameters
        ----------
        parent
            Master for widget.
        """
        tk.Frame.__init__(self, parent)
        headers = ["ID", "Name", "In"]
        widths = [50, None, 100]
        anchors=[None, None, tk.CENTER]
        super().__init__(parent, headers)
        self.set_columns(widths=widths, anchors=anchors)
        self.tree.bind("<Double-1>", self.toggle_item)
        self.tree.bind("<Return>", self.toggle_item)

    def toggle_item(self, event):
        """ Toggle item. """
        if len(self.tree.selection()) == 0:
            return
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        self.tree.item(item, values=(values[0], 'X' if values[1] == '' else ''))
        
    def checked_group_ids(self):
        """ Get IDs of checked groups.
        
        Returns
        -------
        groups_ids : list of str
            IDs of all groups.
        placed_in : list of bool
            True if exam in group, False otherwise.

        """
        placed_in = []
        group_ids = []
        for item in self.tree.get_children():
            group_ids.append(self.tree.item(item, 'text'))
            placed_in.append(self.tree.item(item, 'values')[1] == 'X')
        return group_ids, placed_in
