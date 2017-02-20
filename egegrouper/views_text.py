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
       

class ViewStorageText(ViewStorage):
    """Text view to show common information about storage."""
    def show_data(self):
        """Print information about storage."""
        # data = [exams_num, groups_data, num_in_groups, ungrouped_num]
        exams_num = self.data[0]
        groups_data = self.data[1]
        num_in_groups = self.data[2]
        ungrouped_num = self.data[3]
        t = []
        for row, num in zip(groups_data, num_in_groups):
            t_row = []
            for record in row:
                t_row.append(str(record))
            t_row.append(num)
            t.append(t_row)
        t.append(['','','',''])
        t.append(['','','Ungrouped:',ungrouped_num])
        t.append(['','','Total:',exams_num])
        h = ['ID','Name','Description','Number']
        print('\n' + tabulate(t, headers = h, tablefmt="orgtbl") + '\n')

class ViewExamText(ViewExam):
    """Text view to show details of examination."""
    def show_data(self):
        """Print information about examination."""
        e = self.data
        s = '\nE: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        print(s)

# TODO put it to another file later
import matplotlib.pyplot as plt

class ViewExamPlot(ViewExam):
    """Plot view to show details of examination."""
    def show_data(self):
        """Plot signals of examination with matplotlib."""
        e = self.data
        n = 0
        for m in e.ms:
            for s in m.ss:
                n = n + 1
        i = 0
        for m in e.ms:
            t = m.time
            for s in m.ss:
                i = i + 1
                plt.subplot(n*100 + 10 + i)
                plt.plot(s.x)
                plt.xlim(0,len(s.x))
                plt.grid(True)
                plt.title(t)

        plt.tight_layout()
        plt.show()
        
###########################################
