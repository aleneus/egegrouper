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
        # todo: work with headers

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget

class ViewWhereExamTk(ViewWhereExam):
    """Tk view to show groups where examination is."""
    def show_data(self):
        """Show data."""
        group_records, headers, placed_in = self.data
        rows = [(gr[0], gr[1], 'X' if p else '') for p, gr in zip(placed_in, group_records)]
        headers_ext = headers + ('', )
        tree = self.widget.tree
        tree.delete(*tree.get_children())
        for row in rows:
            tree.insert("", END, text=str(row[0]), values=row[1:])

    def set_widget(self, widget):
        """Set widget."""
        self.widget = widget
