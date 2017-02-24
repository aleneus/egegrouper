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
    
    def __init__(self, controller, master=None):
        super().__init__(master)
        
        self.controller = controller

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
        self.storage_info_table.set_handler(self.group_info)
        
        self.controller.view_storage = ViewTableTk()
        self.controller.view_group = ViewTableTk()        
        self.controller.view_storage.set_widget(self.storage_info_table)

    def open_storage(self):
        """Open storage."""
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
        try:
            item = self.storage_info_table.tree.selection()[0]
            if not self.child_opened():
                self.second_master = Toplevel(self.master)
                self.frame_second = FrameGroupInfo(self.controller, self, self.second_master)
                self.controller.view_group.set_widget(self.frame_second.get_widget())
                self.set_child_opened(True)
            self.controller.group_info(self.storage_info_table.tree.item(item,"text"))
        except IndexError:
            pass

    def close_db_and_exit(self):
        """Close data base and exit."""
        self.controller.close_storage()
        root.quit()

    _child_opened = False
    
    def set_child_opened(self, value):
        self._child_opened = value

    def child_opened(self):
        return self._child_opened


class FrameGroupInfo(Frame):
    controller = None
    
    def __init__(self, controller, parent, master=None):
        super().__init__(master)
        self.parent = parent
        self.pack()
        self.controller = controller
        
        self.master.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.group_info_table = GroupInfoTable(self.master)
        self.group_info_table.pack(side=LEFT, fill=BOTH)
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
        self.master.destroy()
        self.parent.set_child_opened(False)

    def get_widget(self):
        return self.group_info_table

if __name__ == '__main__':
    root = Tk()
    model = GrouperModelSqlite3()
    controller = GrouperController()
    controller.set_model(model)
    
    frame_storage = FrameStorageInfo(controller, root)
    frame_storage.controller = controller
    
    frame_storage.mainloop()
