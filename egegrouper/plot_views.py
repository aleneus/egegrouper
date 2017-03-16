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

"""View for plotting data here."""

import matplotlib.pyplot as plt

class Exam:
    """Plot view to show details of examination."""
    
    def show_data(self, exam):
        """Plot signals of examination with matplotlib.

        Parameters
        ----------
        exam: sme.Examination
            SME examination object.

        """
        plt.ion()
        plt.clf()
        n = 0
        for m in exam.ms:
            for s in m.ss:
                n = n + 1
        i = 0
        for m in exam.ms:
            t = m.time
            for s in m.ss:
                i = i + 1
                plt.subplot(n*100 + 10 + i)
                plt.plot(s.x, 'b', linewidth=1)
                plt.xlim(0,len(s.x))
                plt.grid(True)
                plt.title(t)

        plt.tight_layout()
        plt.show()
