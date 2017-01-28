import sqlite3

class GrouperModel:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.fname = None

    def db_opened(self):
        return self.conn != None
    
    def open_db(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()
        self.fname = file_name

    def close_db(self):
        self.conn.close()
        self.conn = None
        self.fname = None

    def __select(self, query, args):
        res = list(self.c.execute(query, args))
        return res

    def get_groups(self):
        q = "select * from egeg_group;"
        res = self.__select(q, [])
        return res

    def get_group(self, group_id):
        q = "select E.exam_id, E.name, E.diagnosis, E.age, E.gender\
             from examination as E, group_element as GE\
             where GE.exam_id = E.exam_id and GE.group_id = ?\
             order by E.name;"
        res = self.__select(q, [group_id, ])
        return res

    def get_exam(self, exam_id):
        q = "select M.meas_id, M.time from measurement as M\
             where M.exam_id = ?;"
        res = self.__select(q, [exam_id, ])
        return res
