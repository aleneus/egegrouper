#! /usr/bin/env python3
#

import cmd, sys, argparse

from model import *
from terminal_view import *
from plot_view import *
from controller import *

class GrouperShell(cmd.Cmd):
    intro = 'Welcome to the Grouper shell.   Type help or ? to list commands.\n'
    prompt = 'igrouper> '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.aliases = {
            'd' : self.do_db_info,
            'g' : self.do_group_info,
            'e' : self.do_exam_info,
            'ag' : self.do_add_group,
            'dg' : self.do_delete_group,
            'at' : self.do_add_to_group,
            'df' : self.do_delete_from_group,
            'we' : self.do_where_is,
            'aj' : self.do_add_json,
            'ej' : self.do_export_json,
            'de' : self.do_delete_exam
            }

    def default(self, line):
        cmd, arg, line = self.parseline(line)
        if cmd in self.aliases:
            self.aliases[cmd](arg)
        else:
            print("*** Unknown syntax: %s" % line)

    def do_EOF(self, arg):
        print()
        return True

    def do_quit(self, arg):
        """ Close data base and exit.
        """
        grouper.close_db()
        return True

    def do_db_info(self, arg):
        """ Print information about data base.

        Aliases: d
        """
        print(grouper.db_info())

    def do_group_info(self, arg):
        """ group_info id
        
        Print information about group.

        Aliases: g
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        grouper.group_info(cargv[0])

    def do_exam_info(self, arg):
        """ exam_info id
        
        Print information about examination.

        Aliases: e
        """
        cargv = arg.split()
        if len(cargv) < 1:
            print('Few arguments')
            return
        if len(cargv) == 1:
            grouper.exam_info(cargv[0])
        if len(cargv) == 2:
            grouper.exam_info(cargv[0], cargv[1])

    def do_add_group(self, arg):
        """ add_group

        Add new group.

        Aliases: ag
        """
        name = input('Name: ')
        descr = input('Description: ')
        grouper.insert_group(name, descr)

    def do_delete_group(self, arg):
        """ delete_group id

        Delete group

        Aliases: dg
        """
        cargv = arg.split()
        if len(cargv)==0:
            print('Few arguments')
            return
        grouper.delete_group(cargv[0])
        
    def do_add_to_group(self, arg):
        """ add_to_group exam_id group_id

        Add examination to group.

        Aliases: at
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        grouper.add_exam_to_group(cargv[0], cargv[1])

    def do_delete_from_group(self, arg):
        """ delete_from_group exam_id group_id

        Delete examination from group.

        Aliases: df
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        grouper.delete_exam_from_group(cargv[0], cargv[1])

    def do_where_is(self, arg):
        """ where_is id

        Show where is examination.

        Aliases: we
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        grouper.where_is_examination(cargv[0])

    def do_add_sme(self, arg):
        """ add_sme file_name

        Add records from sme data base.
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        grouper.add_sme_db(cargv[0])

    def do_add_gs(self, arg):
        """ add_gs file_name

        Add records from Gastroscan sqlite data base.
        """
        cargv = arg.split()
        grouper.add_gs_db(cargv[0])

    def do_add_json(self, arg):
        """ add_json folder_name

        Add examination from json forder.

        Aliases: aj
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        grouper.add_exam_from_json_folder(cargv[0])

    def do_export_json(self, arg):
        """ export_json folder_name

        Export examination to json forder.

        Aliases: ej
        """
        cargv = arg.split()
        if len(cargv) < 2:
            print('Few arguments')
            return
        exam_id = cargv[0]
        folder_name = cargv[1]
        grouper.export_as_json_folder(exam_id, folder_name)

    def do_delete_exam(self, arg):
        """ delete_exam id

        Delete examination from data base.

        Aliases: de
        """
        cargv = arg.split()
        if len(cargv) == 0:
            print('Few arguments')
            return
        exam_id = cargv[0]
        grouper.delete_exam(exam_id)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Name of data base")
    args = parser.parse_args()

    model = GrouperModel()
    term_view = TerminalView()
    plot_view = PlotView()
    grouper = GrouperController(model, term_view, plot_view)
    
    grouper.open_or_create_db(args.fname)
    
    gshell = GrouperShell()
    gshell.cmdloop()
