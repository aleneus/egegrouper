import sqlite3

class GrouperModel:
    def __init__(self):
        self.conn = None;
        self.cur = None;

    def opened(self):
        if self.conn == None:
            res = False
        else:
            res = True
        return res
    
    def open_db(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()

    def close_db(self):
        self.conn.close()
        self.conn = None

    def __select(self, query, args):
        res = list(self.c.execute(query, args))
        return res

    def get_groups(self):
        q = "select * from egeg_group;"
        res = self.__select(q, [])
        return res
