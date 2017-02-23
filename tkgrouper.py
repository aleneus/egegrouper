#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

from egegrouper.controller import *
from egegrouper.model_sqlite3 import *
from egegrouper.views_tk import *
from egegrouper.view_exam_plot import *

# grouper_tk_widgets

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
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=True)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

class StorageInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "description", "number"]
        headers = ["ID", "Name", "Description", "Num"]
        widths = [50, 100, 200, 50]
        super().__init__(parent, names, headers, widths)

class GroupInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "age", "sex", "diagnosis"]
        headers = ["ID", "Name", "Diagnosis", "Age", "Gender"]
        super().__init__(parent, names, headers)

#################################################################
       

# Application

class Application(Frame):
    """Application class."""

    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()
        self.init_mvc()

    def create_widgets(self):
        """Create widgets."""
        
        # main menu
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open storage", command=self.open_storage)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close_db_and_exit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        self.storage_info_table = StorageInfoTable(root)
        self.storage_info_table.pack(side=LEFT, fill=BOTH)
        self.storage_info_table.tkraise()
        self.storage_info_table.tree.bind("<<TreeviewSelect>>", self.group_info) # TODO: Access to tree.
        self.tk_focusNext()        
        self.group_info_table = GroupInfoTable(root)
        self.group_info_table.pack(side=LEFT, fill=BOTH)
        self.group_info_table.tkraise()
        self.group_info_table.tree.bind("<Double-1>", self.plot_exam) # TODO: Access to tree.
        self.group_info_table.tree.bind("<Return>", self.plot_exam) # TODO: Access to tree.

    def init_mvc(self):
        """Initialization of MVC system."""
        self.grouper = GrouperController()
        self.grouper.set_model(GrouperModelSqlite3())
        # views
        self.grouper.view_storage = ViewTableTk()
        self.grouper.view_storage.set_widget(self.storage_info_table)
        
        self.grouper.view_group = ViewTableTk()
        self.grouper.view_group.set_widget(self.group_info_table)

        self.grouper.view_exam_plot = ViewExamPlot()

    def open_storage(self):
        """Open storage."""
        self.file_opt = options = {}
        options['defaultextension'] = '.sme.sqlite'
        options['filetypes'] = [('all files', '.*'), ('sme db files', '.sme.sqlite')]
        options['initialdir'] = '.'
        options['parent'] = root
        options['title'] = 'Open storage'
        file_name = filedialog.askopenfilename()
        if not file_name:
            return
        self.grouper.open_or_create_storage(file_name)
        self.grouper.storage_info()

    def group_info(self, event):
        """Get and show information about examination in selected group."""
        try:
            item = self.storage_info_table.tree.selection()[0]
            self.grouper.group_info(self.storage_info_table.tree.item(item,"text"))
        except IndexError:
            pass

    def plot_exam(self, event):
        """Plot examination in separate matplotlib window."""
        try:
            item = self.group_info_table.tree.selection()[0]
            self.grouper.plot_exam(self.group_info_table.tree.item(item,"text"))
        except IndexError:
            pass
        
    def close_db_and_exit(self):
        """Close data base and exit."""
        self.grouper.close_storage()
        Tk().quit()


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()
