#! /usr/bin/env python3
#

import cmd, sys

class GrouperShell(cmd.Cmd):
    intro = 'Welcome to the Grouper shell.   Type help or ? to list commands.\n'
    prompt = 'igrouper> '

    def do_test(self, arg):
        'Help string for test command'
        print(arg.split())

    def do_q(self, arg):
        'exit igrouper'
        return True

if __name__ == '__main__':
    GrouperShell().cmdloop()
