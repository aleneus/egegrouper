from egegrouper.view import GrouperView
from tabulate import tabulate

class GrouperViewString(GrouperView):
    """String view. Used for text interface."""
    def message(self, text):
        """Return string with message."""
        return text
        
    def error_message(self, text):
        """Return string with error message."""
        s = 'Error: {}'.format(text)
        return s
    
    def table(self, data, headers = None, width=40):
        """Return string with data from table."""
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
        """Return string with examination text info."""
        s = '\nE: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        return s
    
    def storage(self, exams_num, data, num_in_groups, ungrouped_num):
        """Return string with storage info."""
        t = []
        for row, num in zip(data, num_in_groups):
            t_row = []
            for record in row:
                t_row.append(str(record))
            t_row.append(num)
            t.append(t_row)
        t.append(['','','',''])
        t.append(['','','Ungrouped:',ungrouped_num])
        t.append(['','','Total:',exams_num])
        h = ['ID','Name','Description','Number']
        return '\n' + tabulate(t, headers = h, tablefmt="orgtbl") + '\n'
        
