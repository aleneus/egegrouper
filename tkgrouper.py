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
    
    def __init__(self):
        self.master = Tk()
        self.master.title("EGEGrouper")
        
        menubar = Menu(self.master)
        self.storage_menu = Menu(menubar, tearoff=0)
        self.storage_menu.add_command(label="Open", command=self.open_storage)
        self.storage_menu.add_command(label="Create", command=None, state=DISABLED)
        self.storage_menu.add_command(label="Close", command=None, state=DISABLED)
        self.add_data_submenu = Menu(self.storage_menu, tearoff=0)
        self.add_data_submenu.add_command(label="Add SME sqlite3 DB", command=None, state=DISABLED)
        self.add_data_submenu.add_command(label="Add JSON exam", command=None, state=DISABLED)
        self.add_data_submenu.add_command(label="Add Gastroscan sqlite3 DB", command=None, state=DISABLED)
        self.add_data_submenu.add_command(label="Add Gastroscan TXT export", command=None, state=DISABLED)
        self.storage_menu.add_cascade(label="Add data", menu=self.add_data_submenu)
        self.storage_menu.add_command(label="Exit", command=self.close_db_and_exit)
        menubar.add_cascade(label="Storage", menu=self.storage_menu)
        self.group_menu = Menu(menubar, tearoff=0)
        self.group_menu.add_command(label="Add", command=self.add_group)
        self.group_menu.add_command(label="Edit", command=None, state=DISABLED)
        self.group_menu.add_command(label="Delete", command=self.delete_group)
        menubar.add_cascade(label="Group", menu=self.group_menu)
        #self.group_menu.entryconfig("Edit",state=DISABLED) # to future
        self.exam_menu = Menu(menubar, tearoff=0)
        self.exam_menu.add_command(label="Plot", command=self.plot_exam)
        self.exam_menu.add_command(label="Grouping", command=self.grouping)
        self.exam_menu.add_command(label="Delete", command=None, state=DISABLED)
        self.exam_menu.add_command(label="Merge with", command=None, state=DISABLED)
        self.exam_menu.add_command(label="Export to JSON", command=self.export_json)
        menubar.add_cascade(label="Exam", menu=self.exam_menu)
        self.master.config(menu=menubar)

        controller.view_storage = ViewTableTk()
        controller.view_group = ViewTableTk()
        self.storage_table = StorageTable(self.master)
        self.storage_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.storage_table.tkraise()
        self.storage_table.item_opened.connect(self.group_info)
        controller.view_storage.set_widget(self.storage_table)

        self.group_window = GroupWindow(self.master)
        self.group_window.group_table.item_opened.connect(self.plot_exam)

    def open_storage(self):
        """Open storage and show groups in it."""
        file_name = filedialog.askopenfilename(
            title='Open storage',
            defaultextension = '.sme.sqlite',
            filetypes = [('sme db files', '.sme.sqlite'), ('all files', '.*')],
            parent = self.master,
        )
        if not file_name:
            return
        controller.open_or_create_storage(file_name)
        controller.storage_info()
        self.group_window.group_table.clear()

    def group_info(self, *args):
        """Get and show information about examination in selected group."""
        if self.group_window.master.state() == "withdrawn":
            self.group_window.master.deiconify()
        group_id = self.storage_table.selected_item_text()
        if group_id:
            controller.group_info(group_id)
            self.storage_table.last_group_id = group_id

    def grouping(self):
        """Open grouping dialog stub."""
        exam_id = self.group_window.group_table.selected_item_text()
        if exam_id:
            grouping_dialog = GroupingDialog(self.master, exam_id)
            grouping_dialog.master.transient(self.master)
            grouping_dialog.master.grab_set()
            grouping_dialog.master.wait_window(grouping_dialog.master)
            controller.storage_info()
            group_id = self.storage_table.last_group_id
            if group_id:
                controller.group_info(group_id)

    def export_json(self):
        """Export selected examination to json forder."""
        exam_id = self.group_window.group_table.selected_item_text()
        if not exam_id:
            return
        folder_name = filedialog.askdirectory(
            parent = self.master,
            title = 'JSON folder name',
        )
        if not folder_name:
            return
        controller.export_as_json_folder(exam_id, folder_name)
        
    def add_group(self):
        """Add new group."""
        if not controller.storage_opened():
            return
        group_record_dialog = GroupRecordDialog(self.master)
        group_record_dialog.master.transient(self.master)
        group_record_dialog.master.grab_set()
        group_record_dialog.master.wait_window(group_record_dialog.master)

    def delete_group(self):
        """Delete selected group."""
        if not controller.storage_opened():
            return
        group_id = self.storage_table.selected_item_text()
        if group_id:
            controller.delete_group(group_id)
            controller.storage_info()

    def plot_exam(self, *args):
        """Plot examination in separate matplotlib window."""
        exam_id = self.group_window.group_table.selected_item_text()
        if exam_id:
            controller.plot_exam(exam_id)
                
    def close_db_and_exit(self):
        """Close data base and exit."""
        controller.close_storage()
        self.master.quit()

class GroupWindow:
    """Window for show and select examinations."""
    
    def __init__(self, parent):
        self.master = Toplevel(parent)
        self.master.title("Examinations")
        self.master.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.group_table = GroupTable(self.master)
        self.group_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.group_table.tkraise()
        controller.view_group = ViewTableTk()
        controller.view_group.set_widget(self.group_table)
        controller.view_exam_plot = ViewExamPlot()

    def on_destroy(self):
        """Do not destroy, but withdraw."""
        self.master.withdraw()

class GroupingDialog:
    """Dialog for grouping examinations."""
    
    def __init__(self, parent, exam_id):
        self.master = Toplevel(parent)
        self.master.title("Grouping")
        self.grouping_widget = GroupingTable(self.master)
        self.save_button = Button(self.master, text="Save", width=15, command=self.on_save_button)
        self.cancel_button = Button(self.master, text="Cancel", width=15, command=self.master.destroy)
        self.grouping_widget.pack()
        self.cancel_button.pack(side=RIGHT)
        self.save_button.pack(side=RIGHT)
        
        controller.view_where_exam = ViewWhereExamTk()
        controller.view_where_exam.set_widget(self.grouping_widget)
        controller.where_exam(exam_id)
        self.exam_id = exam_id

    def on_save_button(self):
        """Save button handler."""
        group_ids, placed_in = self.grouping_widget.checked_group_ids()
        controller.group_exam(self.exam_id, group_ids, placed_in)
        self.master.destroy()

class GroupRecordDialog:
    """Dialog for edit group record."""
    
    def __init__(self, parent):
        self.master = Toplevel(parent)
        self.master.title("Edit group")
        self.label1 = Label(self.master, width = 10, text='Name')
        self.label2 = Label(self.master, width = 10, text='Description')
        self.name_entry = Entry(self.master, width = 30)
        self.description_entry = Entry(self.master, width = 30)
        self.save_button = Button(self.master, text="Save", width=15, command=self.on_save_button)
        self.cancel_button = Button(self.master, text="Cancel", width=15, command=self.master.destroy)
        self.label1.pack(side=TOP)
        self.name_entry.pack(side=TOP)
        self.label2.pack(side=TOP)
        self.description_entry.pack(side=TOP)
        self.cancel_button.pack(side=RIGHT)
        self.save_button.pack(side=RIGHT)

    def on_save_button(self):
        """Save button handler."""
        controller.insert_group(self.name_entry.get(), self.description_entry.get())
        controller.storage_info()
        self.master.destroy()

if __name__ == '__main__':
    controller = GrouperController()
    controller.set_model(GrouperModelSqlite3())
    controller.view_message = ViewMessageTk()
    main_window = MainWindow()
    main_window.master.mainloop()
