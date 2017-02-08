class TerminalView:
    def message(self, text):
        print(text)
    
    def db_info(self, db_info):
        print()
        print('Total examinations number: {}'.format(db_info[0]))
        print('Groups number: {}'.format(db_info[1]))
        for gi, gn in zip(db_info[2],db_info[3]):
             print('{} {} ({}): {}'.format(gi[0], gi[1], gi[2], gn))
        print('Ungrouped: {}'.format(db_info[4]))
        print()

    def print_row(self, data):
        for d in data:
            print(d, end=' ')
        print()

    def print_table(self, data):
        print()
        for d in data:
            self.print_row(d)
        print()

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
