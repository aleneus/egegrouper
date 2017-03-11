#! /usr/bin/env python3
#

"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

"""Interactiove command line interface to egegrouper."""

import cmd, sys, argparse, readline
from collections import OrderedDict

import egegmvc.sqlite3_model
import egegmvc.text_views
import egegmvc.plot_views
import egegmvc.controller

class DialogText:
    """Text dialog for input fields values."""
    
    data_dict = None
    
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def set_data_dict(data_dict):
        self.data_dict = data_dict        
    
    def input(self):
        for key in self.data_dict:
            self.data_dict[key] = self.rlineinput(key + ': ', self.data_dict[key])
            
    def rlineinput(self, prompt, prefill=''):
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()
            

class GrouperShell(cmd.Cmd):
    """CLI interface to EGEGrouper."""
    
    prompt = 'igrouper> '

    def __init__(self):
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
            
            'aj' : self.do_add_json,
            'ej' : self.do_export_json
            }

    def default(self, line):
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
        """ Close data base and exit.
        """
        controller.close_storage()
        return True

    def do_db_info(self, arg):
        """ Print information about data base.

        Aliases: d
        """
        controller.storage_info()

    def do_group_info(self, arg):
        """ group_info id [hfa]
        
        Print information about group.

        Aliases: g
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        if self.parse(arg, 'hfa'):
            print('Calc quality stub')
        controller.group_info(cargv[0])

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
        
        Plot signals in examination.

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
        answer = input('Are you shure? (yes/no/y/n): ')
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

    def do_add_sme(self, arg):
        """ add_sme file_name

        Add records from sme data base.
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        controller.add_sme_db(cargv[0])

    def do_add_gs(self, arg):
        """ add_gs file_name

        Add records from Gastroscan sqlite data base.
        """
        cargv = arg.split()
        controller.add_gs_db(cargv[0])

    def do_add_json(self, arg):
        """ add_json folder_name

        Add examination from json forder.

        Aliases: aj
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        controller.add_exam_from_json_folder(cargv[0])

    def do_export_json(self, arg):
        """ export_json exam_id folder_name

        Export examination to json forder.

        Aliases: ej
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        exam_id = cargv[0]
        folder_name = cargv[1]
        controller.export_as_json_folder(exam_id, folder_name)

    def do_delete_exam(self, arg):
        """ delete_exam id

        Delete examination from data base.

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
            print('Something wrong')
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

controller = egegmvc.controller.Controller(egegmvc.sqlite3_model.Model())
controller.view_message = egegmvc.text_views.Message()
controller.view_storage = egegmvc.text_views.Table()
controller.view_group = egegmvc.text_views.Table()
controller.view_exam = egegmvc.text_views.Exam()
controller.view_where_exam = egegmvc.text_views.WhereExam()
controller.view_exam_plot = egegmvc.plot_views.Exam()
        
def main():
    print("""
    EGEGrouper Copyright (C) 2017 Aleksandr Popov

    This program comes with ABSOLUTELY NO WARRANTY; for details type `w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `c' for details.
    """)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Name of data base")
    args = parser.parse_args()
    if not controller.open_or_create_storage(args.fname):
        print("Can't open storage\nExit...\n")
        return
    gshell = GrouperShell()
    gshell.cmdloop()

if __name__ == '__main__':
    main()
