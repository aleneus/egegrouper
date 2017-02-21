#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

from egegrouper.controller import *
from egegrouper.model_sqlite3 import *
from egegrouper.views_tk import *


# my widgets

class TableWidget(Frame):
    """Table widget."""
    def __init__(self, parent, names, headers):
        Frame.__init__(self, parent)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree["columns"] = names[1:]
        for (name, header) in zip(names, headers):
            self.tree.heading(name, text=header)
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=1)
        self.tree.pack()

class StorageInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "description", "number"]
        headers = ["ID", "Name", "Description", "Num"]
        super().__init__(parent, names, headers)

class GroupInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "age", "sex", "diagnosis"]
        headers = ["ID", "Name", "Age", "Gender", "Diagnosis"]
        super().__init__(parent, names, headers)
       

# Application

class Application(Frame):
    """Application class."""

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.init_mvc()

    def create_widgets(self):
        """Create widgets."""
        
        # main menu
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open storage", command=self.open_storage)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu=menubar)

        self.storage_info_table = StorageInfoTable(root)
        self.group_info_table = GroupInfoTable(root)
        self.storage_info_table.pack(side=LEFT, fill=Y)
        self.group_info_table.pack(side=LEFT, fill=Y)

    def init_mvc(self):
        """Initialization of MVC system."""
        self.grouper = GrouperController()
        self.grouper.set_model(GrouperModelSqlite3())
        # views
        self.view_storage = ViewStorageTk()
        self.view_storage.set_widget(self.storage_info_table)
        self.grouper.view_storage = self.view_storage

    def open_storage(self):
        """Open storage."""
        self.file_opt = options = {}
        options['defaultextension'] = '.sme.sqlite'
        options['filetypes'] = [('all files', '.*'), ('sme db files', '.sme.sqlite')]
        options['initialdir'] = '.'
        options['parent'] = root
        options['title'] = 'Open storage'
        file_name = filedialog.askopenfilename()
        if file_name == '':
            return
        self.grouper.open_or_create_storage(file_name)
        self.grouper.storage_info()


root = Tk()
app = Application(root)
app.mainloop()
