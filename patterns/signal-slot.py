def connect(signal, slot):
    signal[0] = slot

def disconnect(signal):
    signal[0] = None

class A:
    some_signal = [None]

    def emit_some_signal(self):
        if not self.some_signal[0]:
            return
        self.some_signal[0]()

class B:
    def some_slot(self):
        print('Slot in class B')

b = B()
a = A()

connect(a.some_signal, b.some_slot)
a.emit_some_signal()

disconnect(a.some_signal)
a.emit_some_signal()
