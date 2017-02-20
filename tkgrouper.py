#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

class Application(Frame):
    """Application class."""

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        # self.init_mvc()

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

    # def init_mvc(self):
        # self.grouper = GrouperController()
        # self.model = GrouperModel()
        # self.grouper.set_model(model)

        # self.widget = some list widget from tk
        # settings for widget, pack, size and so on ...
        # self.view_storage = ViewStorageTk()
        # self.view_storage.set_widget(self.widget)
        # self.grouper.view_storage = self.view_storage

    def open_storage(self):
        """Open storage."""
        self.file_opt = options = {}
        options['defaultextension'] = '.sme.sqlite'
        options['filetypes'] = [('all files', '.*'), ('sme db files', '.sme.sqlite')]
        options['initialdir'] = '.'
        options['parent'] = root
        options['title'] = 'Open storage'
        file_name = filedialog.askopenfilename()

        # self.grouper.open_db()
        # self.grouper.storage_info()


root = Tk()
app = Application(root)
app.mainloop()
