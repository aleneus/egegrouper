# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017-2018 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tk interface to egegrouper."""

import tkinter as tk
from tkinter import messagebox, filedialog

from . import controller
from . import sqlite3_model
from . import tk_views, text_views
from . import plot_views
from . import importers
from . import tk_widgets
from .stats_model import StatsModel
from .stats_controller import StatsController

from .glob import *

from collections import OrderedDict

model = sqlite3_model.Model()
controller = controller.Controller(model)

class MainWindow:
    """Main window. Shows groups and main menu."""
    
    def __init__(self):
        """ Initialization. """
        self.master = tk.Tk()
        self.master.title("EGEGrouper {}".format(VERSION))

        self._make_main_menu()
        self.storage_menu.entryconfig("Import", state=tk.DISABLED)
        self.storage_menu.entryconfig("Close", state=tk.DISABLED)
        self.main_menu.entryconfig("Group", state=tk.DISABLED)
        self.main_menu.entryconfig("Exam", state=tk.DISABLED)
        self.group_menu.entryconfig("Statistics", state=tk.DISABLED)

        self.storage_table = tk_widgets.TableWidget(self.master)
        self.storage_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.storage_table.item_opened.connect(self.group_info)
        self.storage_table.item_selected.connect(self.group_selected)
        storage_view = tk_views.StorageTkView()
        storage_view.widget = self.storage_table
        controller.set_view_storage(storage_view)
        self.group_window = GroupWindow(self.master)
        group_view = tk_views.GroupTkView()
        group_view.widget = self.group_window.group_table
        self.group_window.group_table.item_opened.connect(self.plot_exam)
        self.group_window.group_table.item_selected.connect(self.exam_selected)
        controller.set_view_group(group_view)
        controller.set_view_exam_plot(plot_views.ExamPlotView())

        stats_model = StatsModel()
        stats_model.data_provider = model
        self.stats_controller = StatsController()
        self.stats_controller.model = stats_model
        self.stats_controller.message_view = tk_views.MessageTkView()
        self.stats_controller.status_view = text_views.MessageTextView()
        self.stats_controller.table_view = tk_views.StatsTkView(self.master)

    def _make_main_menu(self):
        self.main_menu = tk.Menu(self.master)
        self.storage_menu = tk.Menu(self.main_menu, tearoff=0)
        self.storage_menu.add_command(label="Open", command=self.open_storage)
        self.storage_menu.add_command(label="Create", command=self.create_storage)
        self.storage_menu.add_command(label="Close", command=self.close_storage)
        self.add_data_submenu = tk.Menu(self.storage_menu, tearoff=0)
        self.add_data_submenu.add_command(label="SME sqlite3 DB", command=self.import_sme)
        self.add_data_submenu.add_command(label="Exam from JSON", command=self.import_json)
        #self.add_data_submenu.add_command(label="TODO: Add Gastroscan sqlite3 DB", command=)
        self.storage_menu.add_cascade(label="Import", menu=self.add_data_submenu)
        self.storage_menu.add_command(label="Exit", command=self.close_db_and_exit)
        self.main_menu.add_cascade(label="Storage", menu=self.storage_menu)
        self.group_menu = tk.Menu(self.main_menu, tearoff=0)
        self.group_menu.add_command(label="Add", command=self.add_group)
        self.group_menu.add_command(label="Edit", command=self.edit_group)
        self.group_menu.add_command(label="Delete", command=self.delete_group)
        self.stats_menu = tk.Menu(self.group_menu, tearoff=0)
        self.stats_menu.add_command(label="Gender", command=self.stats_gender)
        self.stats_menu.add_command(label="Diagnosis", command=self.stats_diagnosis)
        self.stats_menu.add_command(label="Age", command=self.stats_age)
        self.group_menu.add_cascade(label="Statistics", menu=self.stats_menu)
        self.main_menu.add_cascade(label="Group", menu=self.group_menu)
        self.exam_menu = tk.Menu(self.main_menu, tearoff=0)
        self.exam_menu.add_command(label="Plot", command=self.plot_exam)
        self.exam_menu.add_command(label="Grouping", command=self.grouping)
        self.exam_menu.add_command(label="Delete forever", command=self.delete_exam)
        #self.exam_menu.add_command(label="TODO?:Merge with", command=None)
        self.exam_menu.add_command(label="Export to JSON", command=self.export_json)
        self.main_menu.add_cascade(label="Exam", menu=self.exam_menu)
        self.help_menu = tk.Menu(self.main_menu, tearoff=0)
        self.help_menu.add_command(label="About", command=self.about)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.main_menu)

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
        self.group_window.group_table.clear()
        # menu
        self.storage_menu.entryconfig("Import", state=tk.NORMAL)
        self.storage_menu.entryconfig("Close", state=tk.NORMAL)
        self.main_menu.entryconfig("Group", state=tk.NORMAL)
        self.group_menu.entryconfig("Edit", state=tk.DISABLED)
        self.group_menu.entryconfig("Delete", state=tk.DISABLED)
        self.group_menu.entryconfig("Statistics", state=tk.DISABLED)
        self.main_menu.entryconfig("Exam", state=tk.DISABLED)
        
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
        self.group_window.group_table.clear()
        # menu
        self.storage_menu.entryconfig("Import", state=tk.NORMAL)
        self.storage_menu.entryconfig("Close", state=tk.NORMAL)
        self.main_menu.entryconfig("Group", state=tk.NORMAL)
        self.group_menu.entryconfig("Edit", state=tk.DISABLED)
        self.group_menu.entryconfig("Delete", state=tk.DISABLED)
        self.group_menu.entryconfig("Statistics", state=tk.DISABLED)
        self.main_menu.entryconfig("Exam", state=tk.DISABLED)

    def close_storage(self):
        """Close storage and clear widgets."""
        controller.close_storage()
        self.group_window.group_table.clear()
        self.storage_table.clear()
        # menu
        self.storage_menu.entryconfig("Import", state=tk.DISABLED)
        self.storage_menu.entryconfig("Close", state=tk.DISABLED)
        self.main_menu.entryconfig("Group", state=tk.DISABLED)
        self.main_menu.entryconfig("Exam", state=tk.DISABLED)

    def import_sme(self):
        "Add records from sqlite3 data base in SME format."
        file_name = filedialog.askopenfilename(
            title='Open storage',
            filetypes = [('sme db files', '.sme.sqlite'), ('all files', '.*')],
            parent = self.master,
        )
        if not file_name:
            return
        importers.SmeSqliteImporter(controller).do_work(file_name)
        controller.storage_info()

    def import_json(self):
        """Add examination from JSON file."""
        file_name = filedialog.askopenfilename(
            parent = self.master,
            title = 'Add exam from JSON',
            filetypes = [('JSON files', '.json'), ('all files', '.*')],
        )
        if not file_name:
            return
        importers.JsonFileImporter(controller).do_work(file_name)
        controller.storage_info()

    def group_selected(self, *args):
        """Group selected slot. Enable some menu items."""
        # menu
        self.group_menu.entryconfig("Edit", state=tk.NORMAL)
        self.group_menu.entryconfig("Delete", state=tk.NORMAL)
        self.group_menu.entryconfig("Statistics", state=tk.NORMAL)

    def exam_selected(self, *args):
        """Exam selected slot. Enable some menu items."""
        # menu
        self.main_menu.entryconfig("Exam", state=tk.NORMAL)

    def group_info(self, *args):
        """Get and show information about examination in selected group."""
        if self.group_window.master.state() == "withdrawn":
            self.group_window.master.deiconify()
        group_id = self.storage_table.selected_item_text()
        if group_id:
            controller.group_info(group_id)
            self.storage_table.last_group_id = group_id
        # menu
        self.main_menu.entryconfig("Exam", state=tk.DISABLED)

    def grouping(self):
        """Open grouping dialog stub."""
        exam_id = self.group_window.group_table.selected_item_text()
        if not exam_id:
            return

        self.storage_table.remember_selection()
        self.group_window.group_table.remember_selection()
        grouping_dialog = GroupingDialog(self.master, exam_id)
        grouping_dialog.master.transient(self.master)
        grouping_dialog.master.grab_set()
        grouping_dialog.master.wait_window(grouping_dialog.master)
        controller.storage_info()
        controller.group_info(self.storage_table.last_group_id)
        self.storage_table.restore_selection()
        self.group_window.group_table.restore_selection()
        
    def delete_exam(self):
        """Delete exam from storage."""
        exam_id = self.group_window.group_table.selected_item_text()
        if not exam_id:
            return
        if messagebox.askquestion("Delete examination", "Are You shure?", icon='warning') == 'no':
            return
        controller.delete_exam(exam_id)
        self.storage_table.remember_selection()
        self.group_window.group_table.remember_selection()
        controller.storage_info()
        controller.group_info(self.storage_table.last_group_id)
        self.storage_table.restore_selection()
        self.group_window.group_table.restore_selection()

    def export_json(self):
        """Export selected examination to JSON file."""
        exam_id = self.group_window.group_table.selected_item_text()
        if not exam_id:
            return
        file_name = filedialog.asksaveasfilename(
            parent = self.master,
            title = 'Export exam to JSON',
            defaultextension = '.json',
            filetypes = [('JSON files', '.json'), ('all files', '.*')],
        )
        if not file_name:
            return
        controller.export_exam_to_json_file(exam_id, file_name)
        
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
        if group_id=='0':
            return
        self.storage_table.remember_selection()
        data = controller.group_record(group_id)
        group_record_dialog = GroupRecordDialog(self.master, data, group_id)
        group_record_dialog.master.transient(self.master)
        group_record_dialog.master.grab_set()
        group_record_dialog.master.wait_window(group_record_dialog.master)
        self.storage_table.restore_selection()

    def delete_group(self):
        """Delete selected group."""
        group_id = self.storage_table.selected_item_text()
        if not group_id:
            return
        if group_id=='0':
            return
        if messagebox.askquestion("Delete", "Are You shure?", icon='warning') == 'no':
            return
        self.storage_table.remember_selection()
        controller.delete_group(group_id)
        controller.storage_info()
        self.storage_table.restore_selection()

    def plot_exam(self, *args):
        """Plot examination in separate matplotlib window."""
        exam_id = self.group_window.group_table.selected_item_text()
        if exam_id:
            controller.plot_exam(exam_id)
                
    def close_db_and_exit(self):
        """Close data base and exit."""
        controller.close_storage()
        self.master.quit()

    def about(self):
        """Show info about program."""
        about_window = AboutWindow(self.master)
        about_window.master.transient(self.master)
        about_window.master.grab_set()
        about_window.master.wait_window(about_window.master)

    def stats_gender(self):
        """ Calculate and show statistics by gender. """
        group_id = self.storage_table.selected_item_text()
        self.stats_controller.stats('gender', group_id)
        
    def stats_diagnosis(self):
        """ Calculate and show statistics by diagnosis. """
        group_id = self.storage_table.selected_item_text()
        self.stats_controller.stats('diagnosis', group_id)
        
    def stats_age(self):
        """ Calculate and show statistics by age. """
        group_id = self.storage_table.selected_item_text()
        self.stats_controller.stats('age', group_id)

class GroupWindow:
    """Window for show and select examinations."""
    
    def __init__(self, parent):
        """Constructor.

        Create window.

        Parameters
        ----------
        parent
            Master for window.

        """
        self.master = tk.Toplevel(parent)
        self.master.title("Examinations")
        self.master.protocol('WM_DELETE_WINDOW', self.on_destroy)
        self.group_table = tk_widgets.TableWidget(self.master)
        self.group_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def on_destroy(self):
        """Do not destroy, but withdraw."""
        self.master.withdraw()

class GroupingDialog:
    """Dialog for grouping examinations."""
    
    def __init__(self, parent, exam_id):
        """Constructor.
        
        Parameters
        ----------
        parent
            Master.
        exam_id : str
            Examination ID.

        """
        self.exam_id = exam_id
        self.master = tk.Toplevel(parent)
        self.master.title("Grouping")
        self.grouping_widget = tk_widgets.GroupingTable(self.master)
        self.save_button = tk.Button(self.master, text="Save",
                                     width=15, command=self.on_save_button)
        self.cancel_button = tk.Button(self.master, text="Cancel",
                                       width=15, command=self.master.destroy)
        self.grouping_widget.pack()
        self.cancel_button.pack(side=tk.RIGHT)
        self.save_button.pack(side=tk.RIGHT)
        where_exam_view = tk_views.WhereExamTkView()
        where_exam_view.widget = self.grouping_widget
        controller.set_view_where_exam(where_exam_view)
        controller.where_exam(exam_id)

    def on_save_button(self):
        """Save button handler."""
        group_ids, placed_in = self.grouping_widget.checked_group_ids()
        controller.group_exam(self.exam_id, group_ids, placed_in)
        self.master.destroy()

class GroupRecordDialog:
    """Dialog for edit group record."""
    
    def __init__(self, parent, group_record, group_id = None):
        """Constructor.
        
        Parameters
        ----------
        parent
            Master.
        group_record : OrderedDict
            Attributes and values of group.
        group_is : str
            Group ID.

        """
        self.group_id = group_id
        self.group_record = group_record
        self.master = tk.Toplevel(parent)
        self.master.title("Edit group")
        self.labels = []
        self.entries = []
        for key in group_record:
            label = tk.Label(self.master, width = 10, text=key)
            label.pack(side=tk.TOP)
            entry = tk.Entry(self.master, width = 30)
            entry.delete(0, tk.END)
            if group_record[key]:
                entry.insert(0, group_record[key])
            else:
                entry.insert(0, '')
            entry.pack(side=tk.TOP)
            self.labels.append(label)
            self.entries.append(entry)
        self.save_button = tk.Button(self.master, text="Save",
                                     width=15, command=self.on_save_button)
        self.cancel_button = tk.Button(self.master, text="Cancel",
                                       width=15, command=self.master.destroy)
        self.cancel_button.pack(side=tk.RIGHT)
        self.save_button.pack(side=tk.RIGHT)

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

class AboutWindow:
    """Window with short info about the program."""
    def __init__(self, parent):
        """Constructor.

        Create window with info about the program.

        """
        self.master = tk.Toplevel(parent)
        self.master.title("About EGEGrouper")
        label = tk.Label(self.master, text="""
        EGEGrouper Copyright (C) 2017-2018 Aleksandr Popov

        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions.
        """)
        label.pack(side=tk.TOP)
        self.close_button = tk.Button(self.master, text="Close", width=15,
                                      command=self.master.destroy)
        self.close_button.pack(side=tk.TOP)

def main():
    """Entry point."""
    controller.set_view_message(tk_views.MessageTkView())
    
    main_window = MainWindow()
    main_window.master.mainloop()
