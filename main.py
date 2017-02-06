#! /usr/bin/env python3
#

import sys
import argparse
from model import *
from terminal_view import *
from plot_view import *
from controller import *

parser = argparse.ArgumentParser()
parser.add_argument("fname", help="Name of data base")
args = parser.parse_args()

model = GrouperModel()
term_view = TerminalView()
plot_view = PlotView()
grouper = GrouperController(model, term_view, plot_view)

grouper.open_or_create_db(args.fname)

while True:
    cargv = input('> ').split()
    if len(cargv) == 0:
        continue

    if cargv[0] in ['q', 'quit']:
        grouper.close_db()
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

    if cargv[0] in ['at', 'add_to_group']:
        grouper.add_exam_to_group(cargv[1], cargv[2])

    if cargv[0] in ['df', 'delete_from_group']:
        grouper.delete_exam_from_group(cargv[1], cargv[2])

    if cargv[0] in ['we', 'where_is']:
        grouper.where_is_examination(cargv[1])

    if cargv[0] in ['add_sme', ]:
        grouper.add_sme_db(cargv[1])

    if cargv[0] in ['add_gs', ]:
        grouper.add_gs_db(cargv[1])

    if cargv[0] in ['aj', 'add_json']:
        grouper.add_exam_from_json_folder(cargv[1])

    if cargv[0] in ['ej', 'export_json']:
        if len(cargv) < 3:
            term_view.message('Not enouth arguments')
            continue
        exam_id = cargv[1]
        folder_name = cargv[2]
        grouper.export_as_json_folder(exam_id, folder_name)

    if cargv[0] in ['de', 'delete_exam']:
        exam_id = cargv[1]
        grouper.delete_exam(exam_id)
