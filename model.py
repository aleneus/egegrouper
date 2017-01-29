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

    def db_info(self):
        # number of groups
        q = "select count(*)\
             from egeg_group;"
        groups_num = list(self.__select(q, []))[0][0]
        # total number of examinations
        q = "select count(*)\
             from examination"
        exams_total_num = list(self.__select(q, []))[0][0]
        # fields from db
        q = "select *\
             from egeg_group;"
        fields = list(self.__select(q, []))
        # numbers of exams in groups
        num_in_groups = []
        for f in fields:
            q = "select count(E.exam_id)\
                 from examination as E, group_element as GE\
                 where GE.exam_id = E.exam_id and GE.group_id = ?"
            num_in_groups.append(list(self.__select(q, [f[0], ]))[0][0])
        # number of ungrouped examinations
        q = 'select count(exam_id)\
             from examination\
             where exam_id not in (select exam_id from group_element)'
        ungrouped_num = list(self.__select(q, []))[0][0]
        return [exams_total_num, groups_num, fields, num_in_groups, ungrouped_num]

    def group_info(self, group_id):
        if group_id == '0':
            q = 'select exam_id, name, diagnosis, age, gender\
                 from examination\
                 where exam_id not in (select exam_id from group_element)'
            return list(self.__select(q, []))
            
        q = "select E.exam_id, E.name, E.diagnosis, E.age, E.gender\
             from examination as E, group_element as GE\
             where GE.exam_id = E.exam_id and GE.group_id = ?\
             order by E.name;"
        return list(self.__select(q, [group_id, ]))

    def exam_info(self, exam_id):
        q = "select M.meas_id, M.time from measurement as M\
             where M.exam_id = ?;"
        return list(self.__select(q, [exam_id, ]))
