#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

from egegrouper.controller import *
from egegrouper.model_sqlite3 import *
from egegrouper.views_tk import *

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
        self.grouper = GrouperController()
        self.model = GrouperModelSqlite3()
        self.grouper.set_model(self.model)

        self.frame = Frame(self)
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.frame.pack()
        
        self.view_storage = ViewStorageTk()
        self.view_storage.set_widget(self.listbox)
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
