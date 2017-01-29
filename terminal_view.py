class TerminalView:
    def db_info(self, db_info):
        print()
        print('Total examinations number: {}'.format(db_info[0]))
        print('Groups number: {}'.format(db_info[1]))
        for gi, gn in zip(db_info[2],db_info[3]):
             print('{} {} ({}): {}'.format(gi[0], gi[1], gi[2], gn))
        print('Ungrouped: {}'.format(db_info[4]))
        print()

    def group_info(self, g_info):
        print()
        for e_info in g_info:
            print(e_info)
        print()

    def exam_info(self, e_info):
        print()
        for m_info in e_info:
            print(m_info)
        print()
