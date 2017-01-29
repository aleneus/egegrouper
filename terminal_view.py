class TerminalView:
    def db_info(self, groups_info):
        print()
        print('Total examinations number: {}'.format(groups_info[0]))
        print('Groups number: {}'.format(groups_info[1]))
        for gi, gn in zip(groups_info[2],groups_info[3]):
             print('{} {} ({}): {}'.format(gi[0], gi[1], gi[2], gn))
        print('Ungrouped: {}'.format(groups_info[4]))
        print()
