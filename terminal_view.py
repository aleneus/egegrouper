class TerminalView:
    def print_groups_info(self, number, groups_info, ungrouped_number):
        print('=====================')        
        print('Groups number: {}'.format(number))
        print('---------------------')
        for gi in groups_info:
            print('{} | {} ({}): {}'.format(gi[0][0], gi[0][1], gi[0][2], gi[1]))
        print('---------------------')
        print('Ungrouped: {}'.format(ungrouped_number))
        print('=====================')        
