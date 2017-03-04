from tabulate import tabulate

from egegmvc.view import *

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

class ViewWhereExamText(View):
    """Text view to show groups in which selected examination placed."""
    def show_data(self):
        """Show data."""
        group_records, headers, placed_in = self.data
        rows = [('X' if p else '', gr[0], gr[1]) for p, gr in zip(placed_in, group_records)]
        headers_ext = ('', ) + headers
        print('\n' + tabulate(rows, headers=headers_ext, tablefmt="orgtbl") + '\n')
