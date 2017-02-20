from egegrouper.views import *
from tkinter import *
from tkinter import ttk

class ViewStorageTk(ViewStorage):
    """Tk view to show common information about storage."""
    
    def show_data(self):
        """Show information about storage."""
        exams_num, groups_data, num_in_groups, ungrouped_num = self.data
        for (row, num) in zip(groups_data, num_in_groups):
            self.tree.insert("", END, text=str(row[0]), values=(row[1], row[2], num))
        self.tree.insert("", END, text="", values=("", "Ungrouped", ungrouped_num) )
        self.tree.insert("", END, text="", values=("", "Total", exams_num) )

    def set_widget(self, widget):
        """Set widget."""
        self.tree = widget
