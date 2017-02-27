class SimpleSignal:
    """Provides simple qt-like signals and slots mechanism for interconnection with self-made widgets."""
    def __init__(self):
        self.slots = []

    def emit(self, *args):
        """Emit signals"""
        for s in self.slots:
            if s:
                s(args)

    def connect(self, slot):
        """Connect signal with slot."""
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                return
            if self.slots[i] == None:
                self.slots[i] = slot
                return
        self.slots.append(slot)

    def disconnect(self, slot):
        """Disconnect slot from signal."""
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                self.slots[i] = None
