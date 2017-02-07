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

    def do_quit(self, arg):
        """
        Close data base and exit igrouper.

        Aliases: q
        """
        return True
    do_q = do_quit

    def do_db_info(self, arg):
        """
        Print information about data base.

        Aliases: d
        """
        grouper.db_info()
    do_d = do_db_info

    def do_group_info(self, arg):
        """
        Syntax: group_info group_id
        
        Print information about group.

        Aliases: g
        """
        cargv = arg.split()
        grouper.group_info(cargv[0])
    do_g = do_group_info

    def do_exam_info(self, arg):
        """
        Syntax: exam_info exam_id
        
        Print information about examination.

        Aliases: e
        """
        cargv = arg.split()
        if len(cargv) == 1:
            grouper.exam_info(cargv[0])
        if len(cargv) == 2:
            grouper.exam_info(cargv[0], cargv[1])        
    do_e = do_exam_info

    def do_add_group(self, arg):
        """
        Syntax: add_group

        Add new group.

        Aliases: ag
        """
        name = input('Name: ')
        descr = input('Description: ')
        grouper.insert_group(name, descr)
    do_ag = do_add_group

    def do_delete_group(self, arg):
        """
        Syntax: delete_group group_id

        Delete group

        Aliases: dg
        """
        cargv = arg.split()
        grouper.delete_group(cargv[0])
    do_dg = do_delete_group
        
    def do_add_to_group(self, arg):
        """
        Syntax: add_to_group exam_id group_id

        Add examination to group.

        Aliases: at
        """
        cargv = arg.split()        
        grouper.add_exam_to_group(cargv[0], cargv[1])
    do_at = do_add_to_group

    def do_delete_from_group(self, arg):
        """
        Syntax: delete_from_group exam_id group_id

        Delete examination from group.

        Aliases: df
        """
        cargv = arg.split()        
        grouper.delete_exam_from_group(cargv[0], cargv[1])        
    do_df = do_delete_from_group

    def do_where_is(self, arg):
        """
        Syntax: where_is exam_id

        Show where is examination.

        Aliases: we
        """
        cargv = arg.split()        
        grouper.where_is_examination(cargv[0])
    do_we = do_where_is

    def do_add_sme(self, arg):
        """
        Syntax: add_sme file_name

        Add records from sme data base.
        """
        cargv = arg.split()
        grouper.add_sme_db(cargv[0])

    def do_add_gs(self, arg):
        """
        Syntax: add_gs file_name

        Add records from Gastroscan sqlite data base.
        """
        cargv = arg.split()
        grouper.add_gs_db(cargv[0])

    def do_add_json(self, arg):
        """
        Syntax: add_json folder_name

        Add examination from json forder.

        Aliases: aj
        """
        cargv = arg.split()
        grouper.add_exam_from_json_folder(cargv[0])
    do_aj = do_add_json

    def do_export_json(self, arg):
        """
        Syntax: export_json folder_name

        Export examination to json forder.

        Aliases: ej
        """
        cargv = arg.split()
        if len(cargv) < 2:
            term_view.message('Not enouth arguments')
            return
        exam_id = cargv[0]
        folder_name = cargv[1]
        grouper.export_as_json_folder(exam_id, folder_name)
    do_ej = do_export_json

    def do_delete_exam(self, arg):
        """
        Syntax delete_exam exam_id

        Delete examination from data base.

        Aliases: de
        """
        cargv = arg.split()
        exam_id = cargv[0]
        grouper.delete_exam(exam_id)
    do_de = do_delete_exam
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("fname", help="Name of data base")
    args = parser.parse_args()

    model = GrouperModel()
    term_view = TerminalView()
    plot_view = PlotView()
    grouper = GrouperController(model, term_view, plot_view)
    
    grouper.open_or_create_db(args.fname)

    GrouperShell().cmdloop()
