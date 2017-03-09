"""
EGEGrouper - Software for grouping electrogastroenterography examinations.

Copyright (C) 2017 Aleksandr Popov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from tabulate import tabulate

from egegmvc.view import *

class ViewMessageText(View):
    """Text message view."""
    def show_data(self, **kwargs):
        """Print message."""
        print(kwargs['text'])
        

class ViewTableText(View):
    """Text table view."""
    def show_data(self, **kwargs):
        rows = kwargs['data']
        headers = kwargs['headers']
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
       

class ViewExamText(View):
    """Text view to show details of examination."""
    def show_data(self, **kwargs):
        """Print information about examination."""
        e = kwargs['exam']
        s = '\nE: {} {} {} {}\n'.format(e.name, e.gender, e.age, e.diagnosis)
        for m in e.ms:
            s += '    M: {}\n'.format(m.time)
        print(s)

class ViewWhereExamText(View):
    """Text view to show groups in which selected examination placed."""
    def show_data(self, **kwargs):
        """Show data."""
        group_records = kwargs['group_records']
        headers = kwargs['headers']
        placed_in = kwargs['placed_in']
        rows = [('X' if p else '', gr[0], gr[1]) for p, gr in zip(placed_in, group_records)]
        headers_ext = ('', ) + headers
        print('\n' + tabulate(rows, headers=headers_ext, tablefmt="orgtbl") + '\n')
