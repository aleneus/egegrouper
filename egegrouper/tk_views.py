# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017 Aleksandr Popov

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

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class SimpleSignal:
    """Provides simple signals and slots mechanism."""
    def __init__(self):
        """Constructor.

        Create empty list of connected function.
        """
        self.slots = []

    def emit(self, *args):
        """Emit signal."""
        for s in self.slots:
            if s:
                s(args)

    def connect(self, slot):
        """Connect signal with slot.
        
        Parameters
        ----------
        slot
            Function to be connected with signal.
        
        """
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                return
            if self.slots[i] == None:
                self.slots[i] = slot
                return
        self.slots.append(slot)

    def disconnect(self, slot):
        """Disconnect slot from signal.
        
        Parameters
        ----------
        slot
            Name of connected function.
        
        """
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                self.slots[i] = None


class Message:
    """Text message view."""
    def show_data(self, text):
        """ Show message box.

        Parameters
        ----------
        text : str
            Message text.

        """
        messagebox.showinfo("Message", text)
        

class TableWidget(Frame):
    """Table widget."""
    def __init__(self, parent, headers):
        """Constructor.

        Parameters
        ----------
        parent
            Master for widget.
        headers : list of str
            Headers for table.

        """
        Frame.__init__(self, parent)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        self.set_columns(headers)
        # signals
        self.item_opened = SimpleSignal()
        self.tree.bind("<Double-1>", self.item_opened.emit)
        self.tree.bind("<Return>", self.item_opened.emit)
        self.item_selected = SimpleSignal()
        self.tree.bind("<<TreeviewSelect>>", self.item_selected.emit)

    def selected_item_text(self):
        """Return text in selected item.

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

    def set_columns(self, headers):
        """Set number of columns and headers.

        Parameters
        ----------
        headers : list of str
            Headers for table.

        """
        self.tree["columns"] = headers[1:]
        self.tree.heading("#0", text=headers[0])
        for header in headers[1:]:
            self.tree.heading(header, text=header)

    def update_data(self, rows, headers):
        """Fill table with data.

        Parameters
        ----------
        rows : list of tuple of str
            Data in table rows.
        headers : list of str
            Headers.
        
        """
        self.clear()
        for (i, row) in zip(range(len(rows)), rows):
            self.tree.insert("", END, iid = str(i), text=str(row[0]), values=row[1:])

    def clear(self):
        """Clear all items."""
        self.tree.delete(*self.tree.get_children())

    def remember_selection(self):
        """Remember selected item."""
        self._selected_item = self.tree.selection()[0]
        
    def restore_selection(self):
        """Restore selection."""
        if not self.tree.exists(self._selected_item):
            return
        self.tree.selection_set(self._selected_item)
        

class Storage(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        """Constructor.

        Parameters
        ----------
        parent
            Master for widget.

        """
        headers = ["ID", "Name", "Description", "Num"]
        super().__init__(parent, headers)
        self.last_group_id = None
        
    def show_data(self, data, headers):
        """Fill table with data.

        Parameters
        ----------
        data: list of tuples
            Tabular data.
        headers: tuple
            Headers.

        """
        self.update_data(data, headers)

class Group(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        """Constructor.
        
        Parameters
        ----------
        parent
            Master for widget.

        """
        headers = ["ID", "Name", "Diagnosis", "Age", "Gender"]
        super().__init__(parent, headers)
        
    def show_data(self, data, headers):
        """Fill table with data.

        Parameters
        ----------
        data: list of tuples
            Tabular data.
        headers: tuple
            Headers.

        """
        self.update_data(data, headers)
        
class GroupingTable(TableWidget):
    """Table widget for grouping."""
    def __init__(self, parent):
        """Constructor.

        Parameters
        ----------
        parent
            Master for widget.
        """
        Frame.__init__(self, parent)
        headers = ["ID", "Name", "Placed in"]
        super().__init__(parent, headers)
        self.tree.bind("<Double-1>", self.toggle_item)
        self.tree.bind("<Return>", self.toggle_item)

    def toggle_item(self, event):
        """Toggle item."""
        if len(self.tree.selection()) == 0:
            return
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        self.tree.item(item, values=(values[0], 'X' if values[1] == '' else ''))
        
    def checked_group_ids(self):
        """Get IDs of checked groups.
        
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
    
        
class WhereExam(GroupingTable):
    """Tk view to show groups where examination is."""
    
    def show_data(self, group_records, headers, placed_in):
        """Show data.

        Parameters
        ----------
        group_records : list of tuple
            Attributes of groups.
        headers : tuple
            Names of group attributes.
        placed_in : list of bool
            Indicators. True if examination placed in appropriate group, False overwise.

        """
        rows = [
            (gr[0], gr[1], 'X' if p else '')
            for p, gr in zip(placed_in, group_records)
        ]
        headers_ext = headers + ('', )
        self.update_data(rows, headers_ext)
