#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog

from egegrouper.controller import *
from egegrouper.model_sqlite3 import *
from egegrouper.views_tk import *
from egegrouper.view_exam_plot import *
from grouper_tk_widgets import *

class FrameStorageInfo(Frame):
    """Frame to show groups and do operations over them."""
    group_master = None
    group_frame = None
    
    def __init__(self, controller, master=None):
        super().__init__(master)
        
        self.controller = controller

        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open storage", command=self.open_storage)
        filemenu.add_separator()
        filemenu.add_command(label="Add SME sqlite3 DB", command=None)
        filemenu.add_command(label="Add JSON exam", command=None)
        filemenu.add_command(label="Add Gastroscan sqlite3 DB", command=None)
        filemenu.add_command(label="Add Gastroscan TXT export", command=None)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.close_db_and_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        groupmenu = Menu(menubar, tearoff=0)
        groupmenu.add_command(label="Delete", command=None)
        groupmenu.add_command(label="Edit", command=None)
        menubar.add_cascade(label="Group", menu=groupmenu)

        exammenu = Menu(menubar, tearoff=0)
        exammenu.add_command(label="Grouping", command=None)
        exammenu.add_command(label="Delete", command=None)
        exammenu.add_command(label="Merge with", command=None)
        exammenu.add_separator()
        exammenu.add_command(label="Export to JSON", command=None)
        menubar.add_cascade(label="Exam", menu=exammenu)
        
        root.config(menu=menubar)

        self.storage_info_table = StorageInfoTable(root)
        self.storage_info_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.storage_info_table.tkraise()
        self.storage_info_table.set_handler(self.group_info)
        
        self.controller.view_storage = ViewTableTk()
        self.controller.view_group = ViewTableTk()        
        self.controller.view_storage.set_widget(self.storage_info_table)

        self.group_master = Toplevel(self.master)
        self.group_frame = FrameGroupInfo(self.controller, self, self.group_master)

    def open_storage(self):
        """Open storage and show groups in it."""
        self.file_opt = options = {}
        options['defaultextension'] = '.sme.sqlite'
        options['filetypes'] = [('all files', '.*'), ('sme db files', '.sme.sqlite')]
        options['parent'] = self.master
        options['title'] = 'Open storage'
        file_name = filedialog.askopenfilename()
        if not file_name:
            return
        self.controller.open_or_create_storage(file_name)
        self.controller.storage_info()

    def group_info(self, event):
        """Get and show information about examination in selected group."""
        if self.group_master.state() == "withdrawn":
            self.group_master.deiconify()
        try:
            item = self.storage_info_table.tree.selection()[0]
            self.controller.group_info(self.storage_info_table.tree.item(item,"text"))
        except IndexError:
            pass

    def close_db_and_exit(self):
        """Close data base and exit."""
        self.controller.close_storage()
        root.quit()

class FrameGroupInfo(Frame):
    """Frame for show examinations of group and do operations over them."""
    controller = None
    
    def __init__(self, controller, parent, master=None):
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.controller = controller
        
        self.master.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.group_info_table = GroupInfoTable(self.master)
        self.group_info_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.group_info_table.tkraise()
        self.group_info_table.set_handler(self.plot_exam)

        self.controller.view_group = ViewTableTk()
        self.controller.view_group.set_widget(self.group_info_table)
        self.controller.view_exam_plot = ViewExamPlot()

    def plot_exam(self, event):
        """Plot examination in separate matplotlib window."""
        try:
            item = self.group_info_table.tree.selection()[0]
            self.controller.plot_exam(self.group_info_table.tree.item(item,"text"))
        except IndexError:
            pass
        
    def on_destroy(self):
        """Do not destroy, but withdraw."""
        self.master.withdraw()

if __name__ == '__main__':
    root = Tk()
    controller = GrouperController()
    controller.set_model(GrouperModelSqlite3())
    frame_storage = FrameStorageInfo(controller, root)
    frame_storage.controller = controller
    frame_storage.mainloop()
