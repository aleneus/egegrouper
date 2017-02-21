#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

from egegrouper.controller import *
from egegrouper.model_sqlite3 import *
from egegrouper.views_tk import *


# my widgets

class StorageInfoTable(Frame):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree["columns"]=("Name", "Description", "Num")
        self.tree.heading("#0", text="ID")
        self.tree.column("#0", width=50)
        self.tree.column("Name")
        self.tree.heading("Name", text="Name")
        self.tree.column("Description")
        self.tree.heading("Description", text="Description")
        self.tree.column("Num", width=50)
        self.tree.heading("Num", text="Num")
        self.scrollbar.pack(side=RIGHT, fill=Y, expand=1)
        self.tree.pack()
        self.pack()


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

    def init_mvc(self):
        """Initialization of MVC system."""
        self.grouper = GrouperController()
        self.grouper.set_model(GrouperModelSqlite3())
        self.view_storage = ViewStorageTk()
        self.view_storage.set_widget(StorageInfoTable(root))
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
