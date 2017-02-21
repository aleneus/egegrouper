from egegrouper.views import *
from tkinter import *
from tkinter import ttk

class ViewTableTk(ViewTable):
    """Tk view to show tabular data."""
    widget = None
    
    def show_data(self):
        """Fill table with data."""
        rows, headers = self.data
        tree = self.widget.tree
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", END, text=str(row[0]), values=row[1:])

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget

class ViewStorageTk(ViewStorage):
    """Tk view to show common information about storage."""
    widget = None
    
    def show_data(self):
        """Show information about storage."""
        exams_num, groups_data, num_in_groups, ungrouped_num = self.data
        tree = self.widget.tree
        tree.delete(*tree.get_children())
        for (row, num) in zip(groups_data, num_in_groups):
            tree.insert("", END, text=str(row[0]), values=(row[1], row[2], num))
        tree.insert("", END, text="", values=("", "Ungrouped", ungrouped_num))
        tree.insert("", END, text="", values=("", "Total", exams_num))

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget
