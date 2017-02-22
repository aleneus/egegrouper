from tabulate import tabulate

from egegrouper.views import *

class ViewMessageText(ViewMessage):
    """Text message view."""
    def show_data(self):
        """Print message."""
        print(self.data)
        

class ViewTableText(ViewTable):
    """Text table view."""
    def show_data(self):
        # data = [rows, headers] or
        # data = [rows]
        rows = self.data[0]
        if len(self.data) > 1:
            headers = self.data[1]
        else:
            headers = None
        
        t = []
        for row in rows:
            t_row = []
            for record in row:
                t_row.append(str(record)[:40])
            t.append(t_row)
        if headers:
            print('\n' + tabulate(t, headers=headers, tablefmt="orgtbl") + '\n')
        else:
            print('\n' + tabulate(t, tablefmt="orgtbl") + '\n')
       

class ViewExamText(ViewExam):
    """Text view to show details of examination."""
    def show_data(self):
        """Print information about examination."""
        e = self.data
        s = '\nE: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        print(s)
