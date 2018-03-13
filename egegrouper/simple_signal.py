# EGEGrouper - Software for grouping electrogastroenterography examinations.

# Copyright (C) 2017-2018 Aleksandr Popov

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

""" This module implements the SimpleSignal class which makes the
event handling more convenient. """

class SimpleSignal:
    """Provides simple signals and slots mechanism."""
    def __init__(self):
        """Constructor.

        Create empty list of connected function.
        """
        self.slots = []

    def emit(self, *args):
        """Emit signal."""
        for s in self.slots:
            if s:
                s(args)

    def connect(self, slot):
        """Connect signal with slot.
        
        Parameters
        ----------
        slot
            Function to be connected with signal.
        
        """
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                return
            if self.slots[i] == None:
                self.slots[i] = slot
                return
        self.slots.append(slot)

    def disconnect(self, slot):
        """Disconnect slot from signal.
        
        Parameters
        ----------
        slot
            Name of connected function.
        
        """
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                self.slots[i] = None
