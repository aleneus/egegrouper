import sys
from model import *
from terminal_view import *

model = GrouperModel()
term_view = TerminalView()

if len(sys.argv) > 1:
    model.open_db(sys.argv[1])

while True:
    cargv = input('> ').split()

    """ Work with DB
    """
    if cargv[0] in ['o', 'open']:
        if model.db_opened():
            model.close_db()
        model.open_db(cargv[1])
        print('Open data base {} ...'.format(cargv[1]))

    if cargv[0] in ['c', 'close']:
        if model.db_opened():
            model.close_db()
            print('Close data base')

    if cargv[0] in ['q', 'quit']:
        if model.db_opened():
            model.close_db()
        break

    """ Data manipulations
    """
    if cargv[0] in ['gs', 'groups']:
        if not model.db_opened():
            continue
        groups_info = model.get_groups_info()
        term_view.print_groups_info(groups_info)
    
    if cargv[0] in ['sg', 'show_group']:
        if not model.db_opened():
            continue
        res = list(model.get_group(cargv[1]))
        for r in res:
            print(r)

    if cargv[0] in ['se', 'show_exam']:
        if not model.db_opened():
            continue
        res = list(model.get_exam(cargv[1]))
        for r in res:
            print(r)

    if cargv[0] in ['h', 'help']:
        print('EGEGrouper CLI')
