import sys
from model import *

db_name = ''
model = GrouperModel()

if len(sys.argv) > 1:
    db_name = sys.argv[1]
    model.open_db(db_name)

while True:
    cparts = input('> ').split()

    """ Work with DB
    """
    if cparts[0] in ['o', 'open']:
        if model.opened():
            model.close_db()
        db_name = cparts[1]
        model.open_db(db_name)
        print('Open data base {} ...'.format(cparts[1]))
        continue

    if cparts[0] in ['c', 'close']:
        if model.opened():
            model.close_db()
            print('Close data base {}'.format(db_name))
        continue

    if cparts[0] in ['q', 'quit']:
        if model.opened():
            model.close_db()
        break


    """ Data manipulations
    """
    if cparts[0] in ['gs', 'groups']:
        if not model.opened():
            continue
        res = list(model.get_groups())
        for r in res:
            print(r)
        continue
    
    if cparts[0] in ['h', 'help']:
        print('EGEGrouper CLI')
        continue
