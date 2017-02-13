from egegrouper_mvc.view import View

class StringView(View):
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

    def storage(self, db_info):
        s = '\n'
        s += 'Total examinations number: {}\n'.format(db_info[0])
        s += 'Groups number: {}\n'.format(db_info[1])
        for gi, gn in zip(db_info[2],db_info[3]):
             s += '{} {} ({}): {}\n'.format(gi[0], gi[1], gi[2], gn)
        s += 'Ungrouped: {}\n'.format(db_info[4])
        return s

    def exam(self, e):
        s = 'E: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        return s
