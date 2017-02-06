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

    def do_test(self, arg):
        'Help string for test command'
        print(arg.split())

    def do_quit(self, arg):
        """
        Close data base and exit igrouper.

        Aliases: q
        """
        return True
    do_q = do_quit

    # do_d = do_db_info(self, arg):
    
    
    # if cargv[0] in ['d', 'di', 'db_info']:
    #     grouper.db_info()
    

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
