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
from simple_signal import *

class MainWindow:
    """Main window. Shows groups and provide operations via main menu."""
    
    def __init__(self, controller):
        self.controller = controller
        self.master = Tk()
        self.master.title("EGEGrouper")
        
        menubar = Menu(self.master)
        
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
        exammenu.add_command(label="Grouping", command=self.grouping)
        exammenu.add_command(label="Delete", command=None)
        exammenu.add_command(label="Merge with", command=None)
        exammenu.add_separator()
        exammenu.add_command(label="Export to JSON", command=None)
        menubar.add_cascade(label="Exam", menu=exammenu)
        
        self.master.config(menu=menubar)

        self.storage_info_table = StorageInfoTable(self.master)
        self.storage_info_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.storage_info_table.tkraise()
        self.storage_info_table.item_opened.connect(self.group_info)
        
        self.controller.view_storage = ViewTableTk()
        self.controller.view_group = ViewTableTk()        
        self.controller.view_storage.set_widget(self.storage_info_table)

        self.exams_window = GroupInfoWindow(self.controller, self.master)

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
        self.exams_window.group_info_table.clear()

    def group_info(self, *args):
        """Get and show information about examination in selected group."""
        if self.exams_window.master.state() == "withdrawn":
            self.exams_window.master.deiconify()
        group_id = self.storage_info_table.selected_item_text()
        if group_id:
            self.controller.group_info(group_id)

    def grouping(self):
        """Open grouping dialog stub."""
        exam_id = self.exams_window.group_info_table.selected_item_text()
        if exam_id:
            grouping_dialog = GroupingDialog(controller, self.master, exam_id)
            grouping_dialog.master.transient(self.master)
            grouping_dialog.master.grab_set()
            grouping_dialog.master.wait_window(grouping_dialog.master)
            self.controller.storage_info()
            group_id = self.controller.active_group()
            if group_id:
                self.controller.group_info(group_id)
        
    def close_db_and_exit(self):
        """Close data base and exit."""
        self.controller.close_storage()
        self.master.quit()

class GroupInfoWindow:
    """Window for show examinations of group and do operations over them."""
    controller = None
    
    def __init__(self, controller, parent):
        self.controller = controller
        self.master = Toplevel(parent)
        self.master.title("Examinations")
        self.master.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.group_info_table = GroupInfoTable(self.master)
        self.group_info_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.group_info_table.tkraise()
        self.group_info_table.item_opened.connect(self.plot_exam)

        self.group_id = None

        self.controller.view_group = ViewTableTk()
        self.controller.view_group.set_widget(self.group_info_table)
        self.controller.view_exam_plot = ViewExamPlot()

    def plot_exam(self, *args):
        """Plot examination in separate matplotlib window."""
        exam_id = self.group_info_table.selected_item_text()
        if exam_id:
            self.controller.plot_exam(exam_id)
        
    def on_destroy(self):
        """Do not destroy, but withdraw."""
        self.master.withdraw()

class GroupingDialog:
    """Dialog for grouping examinations."""
    
    def __init__(self, controller, parent, exam_id):
        self.master = Toplevel(parent)
        self.master.title("Grouping")
        self.grouping_widget = GroupingTable(self.master)
        self.save_button = Button(self.master, text="Save", width=15, command=self.on_save_button)
        self.cancel_button = Button(self.master, text="Cancel", width=15, command=self.master.destroy)
        
        self.grouping_widget.pack()
        self.cancel_button.pack(side=RIGHT)
        self.save_button.pack(side=RIGHT)
        
        self.controller = controller
        self.controller.view_where_exam = ViewWhereExamTk()
        self.controller.view_where_exam.set_widget(self.grouping_widget)
        
        self.controller.where_exam(exam_id)
        self.exam_id = exam_id

    def on_save_button(self):
        """Save button handler."""
        group_ids, placed_in = self.grouping_widget.checked_group_ids()
        self.controller.group_exam(self.exam_id, group_ids, placed_in)
        self.master.destroy()

if __name__ == '__main__':
    controller = GrouperController()
    controller.set_model(GrouperModelSqlite3())
    main_window = MainWindow(controller)
    main_window.master.mainloop()
