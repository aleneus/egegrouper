from egegrouper_mvc.view import View
from tabulate import tabulate

class ViewString(View):
    def message(self, text):
        return text
        
    def error_message(self, text):
        s = 'Error: {}'.format(text)
        return s
    
    def table(self, data, headers = None, width=30):
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
        s = 'E: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        return s
    
    def storage(self, db_info):
        s = '\n'
        s += 'Total examinations number: {}\n'.format(db_info[0])
        s += 'Groups number: {}\n'.format(db_info[1])
        for gi, gn in zip(db_info[2],db_info[3]):
             s += '{} {} ({}): {}\n'.format(gi[0], gi[1], gi[2], gn)
        s += 'Ungrouped: {}\n'.format(db_info[4])
        return s

