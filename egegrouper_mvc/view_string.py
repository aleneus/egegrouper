from egegrouper_mvc.view import View
from tabulate import tabulate

class ViewString(View):
    def message(self, text):
        return text
        
    def error_message(self, text):
        s = 'Error: {}'.format(text)
        return s
    
    def table(self, data, headers = None, width=40):
        t = []
        for row in data:
            t_row = []
            for record in row:
                t_row.append(str(record)[:width])
            t.append(t_row)
        if headers:
            return '\n' + tabulate(t, headers=headers, tablefmt="orgtbl") + '\n'
        else:
            return '\n' + tabulate(t, tablefmt="orgtbl") + '\n'

    def exam(self, e):
        s = '\nE: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        return s
    
    def storage(self, db_info):
        # [exams_total_num, groups_num, fields, num_in_groups, ungrouped_num]
        t = []
        for row, num in zip(db_info[2], db_info[3]):
            t_row = []
            for record in row:
                t_row.append(str(record))
            t_row.append(num)
            t.append(t_row)
        t.append(['','','',''])
        t.append(['','','Ungrouped:',db_info[4]])
        t.append(['','','Total:',db_info[0]])
        h = ['ID','Name','Description','Number']
        return '\n' + tabulate(t, headers = h, tablefmt="orgtbl") + '\n'

