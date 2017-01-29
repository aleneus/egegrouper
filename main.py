import sys
from model import *
from terminal_view import *
from plot_view import *
from controller import *

model = GrouperModel()
term_view = TerminalView()
plot_view = PlotView()
grouper = GrouperController(model, term_view, plot_view)

if len(sys.argv) > 1:
    model.open_db(sys.argv[1])

while True:
    cargv = input('> ').split()

    # if cargv[0] in ['o', 'open']:
    #     if model.db_opened():
    #         model.close_db()
    #     model.open_db(cargv[1])
    #     print('Open data base {} ...'.format(cargv[1]))

    # if cargv[0] in ['c', 'close']:
    #     if model.db_opened():
    #         model.close_db()
    #         print('Close data base')

    if cargv[0] in ['q', 'quit']:
        model.close_db()
        break

    if cargv[0] in ['d', 'di', 'db_info']:
        grouper.db_info()
    
    if cargv[0] in ['g', 'gi', 'group_info']:
        grouper.group_info(cargv[1])

    if cargv[0] in ['e', 'ei', 'exam_info']:
        if len(cargv) == 2:
            grouper.exam_info(cargv[1])
        if len(cargv) == 3:
            grouper.exam_info(cargv[1], cargv[2])

    if cargv[0] in ['ag', 'add_group']:
        name = input('Name: ')
        descr = input('Description: ')
        grouper.insert_group(name, descr)

    if cargv[0] in ['dg', 'delete_group']:
        grouper.delete_group(cargv[1])

