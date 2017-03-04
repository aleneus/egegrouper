#! /usr/bin/env python3
#

"""Tk interface to egegrouper."""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from egegmvc.controller import *
from egegmvc.models.sqlite3 import *
from egegmvc.views.tk import *
from egegmvc.views.exam_plot import *
from grouper_tk_widgets import *
from simple_signal import *

class MainWindow:
    """Main window. Shows groups and provide operations via main menu."""
    
    def __init__(self):
        self.master = Tk()
        self.master.title("EGEGrouper")
        
        self.main_menu = Menu(self.master)
        self.storage_menu = Menu(self.main_menu, tearoff=0)
        self.storage_menu.add_command(label="Open", command=self.open_storage)
        self.storage_menu.add_command(label="Create", command=self.create_storage)
        self.storage_menu.add_command(label="Close", command=self.close_storage)
        self.add_data_submenu = Menu(self.storage_menu, tearoff=0)
        self.add_data_submenu.add_command(label="Add SME sqlite3 DB", command=self.add_sme)
        self.add_data_submenu.add_command(label="Add JSON folder", command=self.add_json)
        #self.add_data_submenu.add_command(label="TODO: Add Gastroscan sqlite3 DB", command=)
        self.storage_menu.add_cascade(label="Add data", menu=self.add_data_submenu)
        self.storage_menu.add_command(label="Exit", command=self.close_db_and_exit)
        self.main_menu.add_cascade(label="Storage", menu=self.storage_menu)
        self.group_menu = Menu(self.main_menu, tearoff=0)
        self.group_menu.add_command(label="Add", command=self.add_group)
        self.group_menu.add_command(label="Edit", command=self.edit_group)
        self.group_menu.add_command(label="Delete", command=self.delete_group)
        self.main_menu.add_cascade(label="Group", menu=self.group_menu)
        self.exam_menu = Menu(self.main_menu, tearoff=0)
        self.exam_menu.add_command(label="Plot", command=self.plot_exam)
        self.exam_menu.add_command(label="Grouping", command=self.grouping)
        self.exam_menu.add_command(label="Delete forever", command=self.delete_exam)
        #self.exam_menu.add_command(label="TODO?:Merge with", command=None)
        self.exam_menu.add_command(label="Export to JSON", command=self.export_json)
        self.main_menu.add_cascade(label="Exam", menu=self.exam_menu)
        self.master.config(menu=self.main_menu)

        self.storage_menu.entryconfig("Add data", state=DISABLED)
        self.storage_menu.entryconfig("Close", state=DISABLED)
        self.main_menu.entryconfig("Group", state=DISABLED)
        self.main_menu.entryconfig("Exam", state=DISABLED)

        controller.view_storage = ViewTableTk()
        controller.view_group = ViewTableTk()
        self.storage_table = StorageTable(self.master)
        self.storage_table.pack(side=LEFT, fill=BOTH, expand=True)
        self.storage_table.tkraise()
        self.storage_table.item_opened.connect(self.group_info)
        self.storage_table.item_selected.connect(self.group_selected)
        controller.view_storage.set_widget(self.storage_table)

        self.group_window = GroupWindow(self.master)
        self.group_table = self.group_window.group_table
        self.group_table.item_opened.connect(self.plot_exam)
        self.group_table.item_selected.connect(self.exam_selected)
        controller.view_group = ViewTableTk()
        controller.view_group.set_widget(self.group_table)
        controller.view_exam_plot = ViewExamPlot()

    def open_storage(self):
        """Open storage and show groups in it."""
        file_name = filedialog.askopenfilename(
            title='Open storage',
            filetypes = [('sme db files', '.sme.sqlite'), ('all files', '.*')],
            parent = self.master,
        )
        if not file_name:
            return
        controller.open_storage(file_name)
        # menu
        self.storage_menu.entryconfig("Add data", state=NORMAL)
        self.storage_menu.entryconfig("Close", state=NORMAL)
        self.group_table.clear()
        self.main_menu.entryconfig("Group", state=NORMAL)
        self.group_menu.entryconfig("Edit", state=DISABLED)
        self.group_menu.entryconfig("Delete", state=DISABLED)
        self.main_menu.entryconfig("Exam", state=DISABLED)
        
    def create_storage(self):
        """Create storage."""
        file_name = filedialog.asksaveasfilename(
            title='Open storage',
            defaultextension = '.sme.sqlite',
            filetypes = [('sme db files', '.sme.sqlite'), ('all files', '.*')],
            parent = self.master,
        )
        if not file_name:
            return
        controller.create_storage(file_name)
        # menu
        self.storage_menu.entryconfig("Add data", state=NORMAL)
        self.storage_menu.entryconfig("Close", state=NORMAL)
        self.group_table.clear()
        self.main_menu.entryconfig("Group", state=NORMAL)
        self.group_menu.entryconfig("Edit", state=DISABLED)
        self.group_menu.entryconfig("Delete", state=DISABLED)
        self.main_menu.entryconfig("Exam", state=DISABLED)

    def close_storage(self):
        """Close storage and clear widgets."""
        controller.close_storage()
        self.group_table.clear()
        self.storage_table.clear()
        self.storage_menu.entryconfig("Add data", state=DISABLED)
        self.storage_menu.entryconfig("Close", state=DISABLED)
        self.main_menu.entryconfig("Group", state=DISABLED)
        self.main_menu.entryconfig("Exam", state=DISABLED)

    def add_sme(self):
        "Add records from sqlite3 data base in SME format."
        file_name = filedialog.askopenfilename(
            title='Open storage',
            filetypes = [('sme db files', '.sme.sqlite'), ('all files', '.*')],
            parent = self.master,
        )
        if not file_name:
            return
        controller.add_sme_db(file_name)
        controller.storage_info()

    def add_json(self):
        """Add examination from json forder."""
        folder_name = filedialog.askdirectory(
            parent = self.master,
            title = 'JSON folder name',
        )
        if not folder_name:
            return
        controller.add_exam_from_json_folder(folder_name)
        controller.storage_info()

    def group_selected(self, *args):
        """Group selected slot. Enable some menu items."""
        self.group_menu.entryconfig("Edit", state=NORMAL)
        self.group_menu.entryconfig("Delete", state=NORMAL)

    def exam_selected(self, *args):
        """Exam selected slot. Enable some menu items."""
        self.main_menu.entryconfig("Exam", state=NORMAL)

    def group_info(self, *args):
        """Get and show information about examination in selected group."""
        if self.group_window.master.state() == "withdrawn":
            self.group_window.master.deiconify()
        group_id = self.storage_table.selected_item_text()
        if group_id:
            controller.group_info(group_id)
            self.storage_table.last_group_id = group_id
        # menu
        self.main_menu.entryconfig("Exam", state=DISABLED)

    def grouping(self):
        """Open grouping dialog stub."""
        exam_id = self.group_table.selected_item_text()
        if not exam_id:
            return
        grouping_dialog = GroupingDialog(self.master, exam_id)
        grouping_dialog.master.transient(self.master)
        grouping_dialog.master.grab_set()
        grouping_dialog.master.wait_window(grouping_dialog.master)
        controller.storage_info()
        group_id = self.storage_table.last_group_id
        controller.group_info(group_id)

    def delete_exam(self):
        """Delete exam from storage."""
        exam_id = self.group_table.selected_item_text()
        if not exam_id:
            return
        if messagebox.askquestion("Delete examination", "Are You shure?", icon='warning') == 'no':
            return
        controller.delete_exam(exam_id)        
        controller.storage_info()
        group_id = self.storage_table.last_group_id
        controller.group_info(group_id)

    def export_json(self):
        """Export selected examination to json forder."""
        exam_id = self.group_table.selected_item_text()
        if not exam_id:
            return
        folder_name = filedialog.asksaveasfilename(
            parent = self.master,
            title = 'JSON folder name',
            defaultextension = '',
        )
        if not folder_name:
            return
        controller.export_as_json_folder(exam_id, folder_name)
        
    def add_group(self):
        """Add new group."""
        group_record_dialog = GroupRecordDialog(
            self.master,
            group_record = OrderedDict([('name',''), ('description','')])
        )
        group_record_dialog.master.transient(self.master)
        group_record_dialog.master.grab_set()
        group_record_dialog.master.wait_window(group_record_dialog.master)

    def edit_group(self):
        """Edit group."""
        group_id = self.storage_table.selected_item_text()
        if not group_id:
            return
        data = controller.group_record(group_id)
        group_record_dialog = GroupRecordDialog(self.master, data, group_id)
        group_record_dialog.master.transient(self.master)
        group_record_dialog.master.grab_set()
        group_record_dialog.master.wait_window(group_record_dialog.master)

    def delete_group(self):
        """Delete selected group."""
        group_id = self.storage_table.selected_item_text()
        if not group_id:
            return
        if messagebox.askquestion("Delete", "Are You shure?", icon='warning') == 'no':
            return
        controller.delete_group(group_id)
        controller.storage_info()

    def plot_exam(self, *args):
        """Plot examination in separate matplotlib window."""
        exam_id = self.group_table.selected_item_text()
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

    def on_destroy(self):
        """Do not destroy, but withdraw."""
        self.master.withdraw()

class GroupingDialog:
    """Dialog for grouping examinations."""
    
    def __init__(self, parent, exam_id):
        self.exam_id = exam_id
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

    def on_save_button(self):
        """Save button handler."""
        group_ids, placed_in = self.grouping_widget.checked_group_ids()
        controller.group_exam(self.exam_id, group_ids, placed_in)
        self.master.destroy()

class GroupRecordDialog:
    """Dialog for edit group record."""
    
    def __init__(self, parent, group_record, group_id = None):
        self.group_id = group_id
        self.group_record = group_record
        self.master = Toplevel(parent)
        self.master.title("Edit group")
        self.labels = []
        self.entries = []
        for key in group_record:
            label = Label(self.master, width = 10, text=key)
            label.pack(side=TOP)
            entry = Entry(self.master, width = 30)
            entry.delete(0, END)
            if group_record[key]:
                entry.insert(0, group_record[key])
            else:
                entry.insert(0, '')
            entry.pack(side=TOP)
            self.labels.append(label)
            self.entries.append(entry)
        self.save_button = Button(self.master, text="Save", width=15, command=self.on_save_button)
        self.cancel_button = Button(self.master, text="Cancel", width=15, command=self.master.destroy)
        self.cancel_button.pack(side=RIGHT)
        self.save_button.pack(side=RIGHT)

    def on_save_button(self):
        """Save button handler."""
        for (key, e) in zip(self.group_record, self.entries):
            self.group_record[key] = e.get()
        if not self.group_id:
            controller.insert_group(self.group_record['name'], self.group_record['description'])
        else:
            controller.update_group_record(self.group_id, self.group_record)
        controller.storage_info()
        self.master.destroy()

if __name__ == '__main__':
    controller = GrouperController()
    controller.set_model(GrouperModelSqlite3())
    controller.view_message = ViewMessageTk()
    main_window = MainWindow()
    main_window.master.mainloop()
