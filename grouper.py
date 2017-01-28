import sqlite3
import sys

db_name = ''
conn = None
cur = None

if len(sys.argv) > 1:
    db_name = sys.argv[1]
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

def check_db():
    res = (db_name != '')
    if res == False:
        print('Fisrt open data base')
    return res

while True:
    cparts = input('> ').split()

    """ Work with DB
    """
    if cparts[0] in ['o', 'open']:
        if check_db:
            conn.close()
        db_name = cparts[1]
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        print('Open data base {} ...'.format(cparts[1]))
        continue

    if cparts[0] in ['c', 'close']:
        if db_name == '':
            print('Fisrt open data base')
            continue
        conn.close()
        db_name = ''
        print('Close data base {}'.format(db_name))
        continue

    if cparts[0] in ['q', 'quit']:
        if db_name != '':
            conn.close()
        break


    """ Data manipulations
    """
    if cparts[0] in ['gs', 'groups']:
        if not check_db():
            continue
        res = list(cur.execute('select * from egeg_group;'))
        for r in res:
            print(r)
        continue
    
    if cparts[0] in ['h', 'help']:
        print('EGEGrouper CLI')
        continue
