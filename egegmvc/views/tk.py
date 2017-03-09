"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from egegmvc.view import *


class SimpleSignal:
    """Provides simple signals and slots mechanism for interconnection with self-made widgets."""
    def __init__(self):
        self.slots = []

    def emit(self, *args):
        """Emit signals"""
        for s in self.slots:
            if s:
                s(args)

    def connect(self, slot):
        """Connect signal with slot."""
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                return
            if self.slots[i] == None:
                self.slots[i] = slot
                return
        self.slots.append(slot)

    def disconnect(self, slot):
        """Disconnect slot from signal."""
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                self.slots[i] = None


class ViewMessageTk(View):
    """Text message view."""
    def show_data(self, data):
        """Print message."""
        messagebox.showinfo("Message", data)
        

class TableWidget(Frame):
    """Table widget."""
    def __init__(self, parent, names, headers, widths = []):
        Frame.__init__(self, parent)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree["columns"] = names[1:]
        for (name, header) in zip(names, headers):
            self.tree.heading(name, text=header)
        if len(widths) == len(names):
            for (name, width) in zip(names, widths):
                self.tree.column(name, width=width)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # signals
        self.item_opened = SimpleSignal()
        self.tree.bind("<Double-1>", self.item_opened.emit)
        self.tree.bind("<Return>", self.item_opened.emit)
        self.item_selected = SimpleSignal()
        self.tree.bind("<<TreeviewSelect>>", self.item_selected.emit)

    def selected_item_text(self):
        """Return text in selected item."""
        try:
            item = self.tree.selection()[0]
            item_text = self.tree.item(item,"text")
        except IndexError:
            item_text = None
        finally:
            return item_text

    def update_data(self, rows, headers):
        """Fill table with data."""
        self.clear()
        tree = self.tree
        for row in rows:
            tree.insert("", END, text=str(row[0]), values=row[1:])

    def clear(self):
        """Clear all items."""
        self.tree.delete(*self.tree.get_children())
        

class ViewStorageTk(View, TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "description", "number"]
        headers = ["ID", "Name", "Description", "Num"]
        widths = [50, 100, 200, 50]
        super().__init__(parent, names, headers, widths)
        self.last_group_id = None
        
    def show_data(self, data):
        """Fill table with data."""
        rows, headers = data
        self.update_data(rows, headers)        

class ViewGroupTk(View, TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "age", "sex", "diagnosis"]
        headers = ["ID", "Name", "Diagnosis", "Age", "Gender"]
        super().__init__(parent, names, headers)
        
    def show_data(self, data):
        """Fill table with data."""
        rows, headers = data
        self.update_data(rows, headers)        
        
class GroupingTable(TableWidget):
    """Table widget for grouping."""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        names = ["#0", "name", "in"]
        headers = ["ID", "Name", ""]
        super().__init__(parent, names, headers)
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
        placed_in = []
        group_ids = []
        for item in self.tree.get_children():
            group_ids.append(self.tree.item(item, 'text'))
            placed_in.append(self.tree.item(item, 'values')[1] == 'X')
        return group_ids, placed_in
    
        
class ViewWhereExamTk(View, GroupingTable):
    """Tk view to show groups where examination is."""
    
    def show_data(self, data):
        """Show data."""
        group_records, headers, placed_in = data
        rows = [
            (gr[0], gr[1], 'X' if p else '')
            for p, gr in zip(placed_in, group_records)
        ]
        headers_ext = headers + ('', )
        self.update_data(rows, headers_ext)
