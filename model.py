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
        res = list(self.__select(q, []))
        return res

    def get_groups_info(self):
        q = "select *\
             from egeg_group;"
        groups_info = list(self.__select(q, []))
        number = len(groups_info)
        q = "select count(*)\
             from examination"
        exams_total_number = list(self.__select(q, []))[0][0]
        print(exams_total_number)
        numbers = []
        for gi in groups_info:
            q = "select count(E.exam_id)\
                 from examination as E, group_element as GE\
                 where GE.exam_id = E.exam_id and GE.group_id = ?"
            res = list(self.__select(q, [gi[0], ]))
            numbers.append(res[0][0])
        groups_info = zip(groups_info, numbers)
        q = 'select count(exam_id)\
             from examination\
             where exam_id not in (select exam_id from group_element)'
        ungrouped_number = list(self.__select(q, []))[0][0]
        return (number, groups_info, ungrouped_number)

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
