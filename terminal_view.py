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

    def print_list(self, data):
        print()
        for d in data:
            for item in d:
                print(item, end=' ')
            print()
        print()

    def group_info(self, g_info):
        self.print_list(g_info)

    def exam_info(self, e_info):
        self.print_list(e_info)

