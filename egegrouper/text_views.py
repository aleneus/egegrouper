# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tabulate import tabulate

class Message:
    """Text message view."""
    def show_data(self, text):
        """Print message.
        
        Parameters
        ----------
        text : str
            Text for printing.

        """
        print(text)
        

class Table:
    """Text table view."""
    def show_data(self, data, headers):
        """Show table with headers.

        Parameters
        ----------
        data: list of tuples
            Tabular data.
        headers: tuple
            Headers.
 
        """
        t = []
        for row in data:
            t_row = []
            for record in row:
                t_row.append(str(record)[:40])
            t.append(t_row)
        if headers:
            print('\n' + tabulate(t, headers=headers, tablefmt="orgtbl") + '\n')
        else:
            print('\n' + tabulate(t, tablefmt="orgtbl") + '\n')
       

class Exam:
    """Text view to show details of examination."""
    def show_data(self, exam):
        """Print information about examination.
        
        Parameters
        ----------
        exam: sme.Examination
            SME examination object.

        """
        s = '\nE: {} {} {} {}\n'.format(exam.name, exam.gender, exam.age, exam.diagnosis)
        for m in exam.ms:
            s += '    M: {}\n'.format(m.time)
        print(s)

class WhereExam:
    """Text view to show groups in which selected examination placed."""
    def show_data(self, group_records, headers, placed_in):
        """Show all groups and indicate where the object is located.

        Parameters
        ----------
        group_records : list of tuple
            Attributes of groups.
        headers : tuple
            Names of group attributes.
        placed_in : list of bool
            Indicators. True if examination placed in appropriate group, False overwise.

        """
        rows = [('X' if p else '', gr[0], gr[1]) for p, gr in zip(placed_in, group_records)]
        headers_ext = ('', ) + headers
        print('\n' + tabulate(rows, headers=headers_ext, tablefmt="orgtbl") + '\n')
