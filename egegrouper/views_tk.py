from egegrouper.views import *
from tkinter import *
from tkinter import ttk

class ViewStorageTk(ViewStorage):
    """Tk view to show common information about storage."""
    
    def show_data(self):
        """Show information about storage."""
        # data = [exams_num, groups_data, num_in_groups, ungrouped_num]
        
        exams_num = self.data[0]
        groups_data = self.data[1]
        num_in_groups = self.data[2]
        ungrouped_num = self.data[3]

        for row in groups_data:
            self.tree.insert("", END, text=str(row[0]), values=row[1:])

    def set_widget(self, widget):
        """Set widget."""
        self.tree = widget
