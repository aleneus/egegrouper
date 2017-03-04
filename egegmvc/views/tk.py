from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from egegmvc.view import *

class ViewMessageTk(ViewMessage):
    """Text message view."""
    def show_data(self):
        """Print message."""
        messagebox.showinfo("Message", self.data)

class ViewTableTk(ViewTable):
    """Tk view to show tabular data."""
    
    def show_data(self):
        """Fill table with data."""
        rows, headers = self.data
        self.widget.update_data(rows, headers)

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget

class ViewWhereExamTk(ViewWhereExam):
    """Tk view to show groups where examination is."""
    
    def show_data(self):
        """Show data."""
        group_records, headers, placed_in = self.data
        rows = [
            (gr[0], gr[1], 'X' if p else '')
            for p, gr in zip(placed_in, group_records)
        ]
        headers_ext = headers + ('', )
        self.widget.update_data(rows, headers_ext)

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget
