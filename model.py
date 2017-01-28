import sqlite3

class GrouperModel:
    def open_db(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.c = self.conn.cursor()

    def close_db(self):
        self.conn.close()

    def __select(self, query, args):
        res = list(self.c.execute(query, args))
        return res

    def get_groups(self):
        q = "select * from egeg_groups;"
        res = self.__select(q, [number])
        return res
