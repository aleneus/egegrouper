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

"""Interactive command line interface to EGEGrouper."""

import cmd, sys, argparse, readline
from collections import OrderedDict

from . import sqlite3_model
from . import text_views
from . import plot_views
from . import controller
from . import importers
from .stats_model import StatsModel
from .stats_controller import StatsController

from .glob import *


class DialogText:
    """Text dialog for input fields values. 

    This dialog processes data in the dictionary with keys which
    correspond attributes of group.

    """
    def __init__(self, data_dict):
        """Constructor.

        Parameters
        ----------
        data_dict : OrderedDict
            Dictionary to process.

        """
        self.data_dict = data_dict

    def input(self):
        """Process input data."""
        for key in self.data_dict:
            self.data_dict[key] = self.rlineinput(key + ': ', self.data_dict[key])
            
    def rlineinput(self, prompt, prefill=''):
        """Output existing value to the edit area."""
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()
            

class GrouperShell(cmd.Cmd):
    """Class for processing user's commands."""
    
    prompt = 'igrouper> '

    def __init__(self):
        """Constructor.

        Set aliases for commands.
        """
        cmd.Cmd.__init__(self)
        self.aliases = {
            'd' : self.do_db_info,
            'g' : self.do_group_info,
            'e' : self.do_exam_info,
            'p' : self.do_plot_exam,
            
            'ag' : self.do_add_group,
            'dg' : self.do_delete_group,
            'at' : self.do_add_to_group,
            'df' : self.do_delete_from_group,
            'we' : self.do_where_is,
            
            'ij' : self.do_import_json,
            'ej' : self.do_export_json
            }

    def default(self, line):
        """This method called if user gives not existing command.

        Here the aliases processed.

        Parameters
        ----------
        line : str
            User's command.

        """
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            print("*** Unknown syntax: %s" % line)

    def parse(self, arg, option_name, has_value = False):
        args = arg.split()
        for (a, i) in zip(args, range(0, len(args))):
            if (a == option_name):
                if not has_value:
                    return True
                else:
                    if len(args) > i+1:
                        return args[i+1]
        return None

    def do_EOF(self, arg):
        print()
        return True

    def do_quit(self, arg):
        """ Close database and exit.
        """
        controller.close_storage()
        return True

    def do_db_info(self, arg):
        """ Print information about database.

        Aliases: d
        """
        controller.storage_info()

    def do_group_info(self, arg):
        """ group_info id
        
        Print information about group.

        Aliases: g
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        controller.group_info(cargv[0])

    def do_stats(self, arg):
        """ stats [age|gender|diagnosis] group_id

        Print some statistic of group.

        Special values for group_id:

            0 - Ungrouped exams.
            * - All exams.

        Examples:

            stats gender 1
            stats diagnosis 0
            stats age *
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        key, group_id = cargv[:2]
        stats_controller.stats(key, group_id)
        # TODO: Error if input wrong id
        # TODO: One command or several?

    def do_exam_info(self, arg):
        """ exam_info id
        
        Print information about examination.

        Aliases: e
        """
        cargv = arg.split()
        if len(cargv) < 1:
            print('Few arguments')
            return
        controller.exam(cargv[0])

    def do_plot_exam(self, arg):
        """ plot_exam id
        
        Plot signals of examination.

        Aliases: p
        """
        cargv = arg.split()
        if len(cargv) < 1:
            print('Few arguments')
            return
        controller.plot_exam(cargv[0])
            
    def do_add_group(self, arg):
        """ add_group

        Add new group.

        Aliases: ag
        """
        data = OrderedDict([('Name', ''), ('Description', '')])
        DialogText(data).input()
        controller.insert_group(data['Name'], data['Description'])

    def do_delete_group(self, arg):
        """ delete_group id

        Delete group

        Aliases: dg
        """
        cargv = arg.split()
        if len(cargv)==0:
            print('Few arguments')
            return
        answer = input('Are you sure? (yes/no/y/n): ')
        if answer not in ['yes', 'y']:
            return
        controller.delete_group(cargv[0])
        
    def do_add_to_group(self, arg):
        """ add_to_group exam_id group_id

        Add examination to group.

        Aliases: at
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        controller.group_exam(cargv[0], [cargv[1], ], [True, ])

    def do_delete_from_group(self, arg):
        """ delete_from_group exam_id group_id

        Delete examination from group.

        Aliases: df
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        controller.group_exam(cargv[0], [cargv[1], ], [False, ])

    def do_where_is(self, arg):
        """ where_is id

        Show where is examination.

        Aliases: we
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        controller.where_exam(cargv[0])

    def do_import_sme(self, arg):
        """ import_sme file_name

        Add records from SME database.
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        file_name = cargv[0]
        importers.SmeSqliteImporter(controller).do_work(file_name)

    def do_import_gs(self, arg):
        """ import_gs file_name

        Import records from Gastroscan sqlite database.
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        file_name = cargv[0]
        importers.GsSqliteImporter(controller).do_work(file_name)

    def do_import_json(self, arg):
        """ import_json file_name

        Add examination from JSON file.

        Aliases: aj
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        file_name = cargv[0]
        importers.JsonFileImporter(controller).do_work(file_name)

    def do_export_json(self, arg):
        """ export_json exam_id file_name

        Export examination to JSON file.

        Aliases: ej
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        exam_id = cargv[0]
        folder_name = cargv[1]
        controller.export_exam_to_json_file(exam_id, folder_name)

    def do_delete_exam(self, arg):
        """ delete_exam id

        Delete examination from database.

        Aliases: de
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        
        answer = input('Are you sure? (yes/no/y/n): ')
        if answer not in ['yes', 'y']:
            return
        
        exam_id = cargv[0]
        controller.delete_exam(exam_id)

    def do_merge_exams(self, arg):
        """ merge_exams exam_id_1 exam_id_2

        Merge two examinations."""
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        exam_id_1 = cargv[0]
        exam_id_2 = cargv[1]
        controller.merge_exams(exam_id_1, exam_id_2)

    def do_edit_group(self, arg):
        """edit_group group_id

        Edit attributes of selected group.
        
        """
        cargv = arg.split()
        if len(cargv) < 1:
            print('Few arguments')
            return
        group_id = cargv[0]
        
        data = controller.group_record(group_id)
        if not data:
            return
        DialogText(data).input()
        controller.update_group_record(group_id, data)

    def do_c(self, arg):
        print("""
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
        """)

    def do_w(self, arg):
        print("""
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
        """)    

# TODO: next is bad in global space, refactor
model = sqlite3_model.Model()
controller = controller.Controller(model)
stats_model = StatsModel()
stats_model.data_provider = model
stats_controller = StatsController()
stats_controller.model = stats_model


def main():
    """Entry point."""
    
    print("""
    EGEGrouper {} Copyright (C) 2017-2018 Aleksandr Popov

    This program comes with ABSOLUTELY NO WARRANTY; for details type `w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `c' for details.
    """.format(VERSION))

    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Name of database")
    args = parser.parse_args()
    
    controller.set_view_message(text_views.MessageTextView())
    controller.set_view_storage(text_views.StorageTextView())
    controller.set_view_group(text_views.GroupTextView())
    controller.set_view_exam(text_views.ExamTextView())
    controller.set_view_where_exam(text_views.WhereExamTextView())
    controller.set_view_exam_plot(plot_views.ExamPlotView())

    if not controller.open_or_create_storage(args.fname):
        print("Can't open storage\nExit...\n")
        return

    # TODO: use common view with controller
    stats_controller.message_view = text_views.MessageTextView()
    stats_controller.status_view = text_views.MessageTextView()
    stats_controller.table_view = text_views.StatsTextView()

    gshell = GrouperShell()
    gshell.cmdloop()
