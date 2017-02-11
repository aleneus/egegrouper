class TerminalView:
    def message(self, text):
        print(text)
    
    def db_info(self, db_info):
        s = '\n'
        s += 'Total examinations number: {}\n'.format(db_info[0])
        s += 'Groups number: {}\n'.format(db_info[1])
        for gi, gn in zip(db_info[2],db_info[3]):
             s += '{} {} ({}): {}\n'.format(gi[0], gi[1], gi[2], gn)
        s += 'Ungrouped: {}\n'.format(db_info[4])
        return s

    def print_row(self, data):
        for d in data:
            print(d, end=' ')
        print()

    def print_table(self, data):
        print()
        for d in data:
            self.print_row(d)
        print()

    def table(self, data):
        s = '\n'
        for row in data:
            s += '{:>5d} | '.format(row[0])
            for record in row[1:]:
                s += '{} '.format(record)
            s += '\n'
        s += '\n'
        return s

    def exam_info(self, e_info):
        print()
        e = e_info
        print('E: ', end = '')
        self.print_row(e[0])
        for m in e[1]:
            print('  M: ', end = '')
            self.print_row(m[0])
            for s in m[1]:
                print('    S: ', end = '')
                # s = list(s)
                # if s[1] == 0:
                #     s[1] = 'Source'
                # else:
                #     s[1] = 'Edited'
                self.print_row(s)
        print()
