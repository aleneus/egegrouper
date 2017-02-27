class SimpleSignal:
    def __init__(self):
        self.slots = []

    def emit(self, *args):
        for s in self.slots:
            if s:
                s(args)

    def connect(self, slot):
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                return
            if self.slots[i] == None:
                self.slots[i] = slot
                return
        self.slots.append(slot)

    def disconnect(self, slot):
        for i in range(len(self.slots)):
            if self.slots[i] == slot:
                self.slots[i] = None

class A:
    some_signal = SimpleSignal()

class B:
    def some_slot(self, *args):
        print('Slot in class B')
        print('Arguments:', args)

class C:
    def some_slot(self, *args):
        print('Slot in class C')
        print('Arguments:', args)
    

a = A()
b = B()
c = C()

a.some_signal.connect(b.some_slot)
a.some_signal.connect(c.some_slot)
a.some_signal.emit(1, 2, 3)

print()
a.some_signal.disconnect(b.some_slot)
a.some_signal.emit(1, 2, 3)

print()
a.some_signal.connect(b.some_slot)
a.some_signal.emit(1, 2, 3)
