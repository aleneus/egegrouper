from view import *

class TerminalView(View):
    def message(self, text):
        return text
        
    def error_message(self, text):
        s = 'Error: {}'.format(text)
        return s
    
    def row(self, data):
        s = ''
        for d in data:
            s += '{} '.format(d)
        return s

    def table(self, data):
        s = '\n'
        for row in data:
            s += '{:>5d} | '.format(row[0])
            for record in row[1:]:
                s += '{} '.format(record)
            s += '\n'
        return s

    def db(self, db_info):
        s = '\n'
        s += 'Total examinations number: {}\n'.format(db_info[0])
        s += 'Groups number: {}\n'.format(db_info[1])
        for gi, gn in zip(db_info[2],db_info[3]):
             s += '{} {} ({}): {}\n'.format(gi[0], gi[1], gi[2], gn)
        s += 'Ungrouped: {}\n'.format(db_info[4])
        return s

    def exam(self, e_info):
        res = '\n'
        e = e_info
        res += 'E: '
        res += self.row(e[0])
        res += '\n'
        for m in e[1]:
            res += '  M: '
            res += self.row(m[0])
            res += '\n'
            for s in m[1]:
                res += '    S: '
                res += self.row(s)
                res += '\n'
        return res
