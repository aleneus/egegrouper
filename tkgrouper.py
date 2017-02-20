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

    def open_storage(self):
        """Open storage."""
        self.file_opt = options = {}
        options['defaultextension'] = '.sme.sqlite'
        options['filetypes'] = [('all files', '.*'), ('sme db files', '.sme.sqlite')]
        options['initialdir'] = '.'
        options['parent'] = root
        options['title'] = 'Open storage'
        file_name = filedialog.askopenfilename()

        # self.frame = Frame(self)
        # self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        # self.listbox = Listbox(self.frame, yscrollcommand=self.scrollbar.set)
        # self.scrollbar.config(command=self.listbox.yview)
        # self.scrollbar.pack(side=RIGHT, fill=Y)
        # self.listbox.pack(side=LEFT, fill=BOTH, expand=1)
        # self.frame.pack()

root = Tk()
app = Application(root)
app.mainloop()
