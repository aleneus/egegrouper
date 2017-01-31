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
    grouper.open_or_create_db(sys.argv[1])

while True:
    cargv = input('> ').split()
    if len(cargv) == 0:
        continue

    """ Quit and help
    """

    if cargv[0] in ['q', 'quit']:
        grouper.close_db()
        break

    """ Get info
    """

    if cargv[0] in ['d', 'di', 'db_info']:
        grouper.db_info()
    
    if cargv[0] in ['g', 'gi', 'group_info']:
        grouper.group_info(cargv[1])

    if cargv[0] in ['e', 'ei', 'exam_info']:
        if len(cargv) == 2:
            grouper.exam_info(cargv[1])
        if len(cargv) == 3:
            grouper.exam_info(cargv[1], cargv[2])


    if cargv[0] in ['et', 'eit', 'exam_info_test']:
        if len(cargv) == 2:
            grouper.exam_info_test(cargv[1])
        if len(cargv) == 3:
            grouper.exam_info(cargv[1], cargv[2])

    """  Data manipulations
    """

    if cargv[0] in ['ag', 'add_group']:
        name = input('Name: ')
        descr = input('Description: ')
        grouper.insert_group(name, descr)

    if cargv[0] in ['dg', 'delete_group']:
        grouper.delete_group(cargv[1])

    if cargv[0] in ['at', 'add_to_group']:
        grouper.add_to_group(cargv[1], cargv[2])

    if cargv[0] in ['df', 'delete_from_group']:
        grouper.delete_from_group(cargv[1], cargv[2])

    if cargv[0] in ['we', 'where_is']:
        grouper.where_is_examination(cargv[1])

    """ Import and export
    """

    if cargv[0] in ['add_sme', ]:
        grouper.add_data_from_sme(cargv[1])
