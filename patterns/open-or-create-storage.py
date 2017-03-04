class Model:
    def storage_exists(self):
        exists = storage_exists
        return exists
    
    def open_storage(self):
        print("opened")

    def create_storage(self):
        print("created")

    def open_or_create_storage(self):
        if self.storage_exists():
            self.open_storage()
        else:
            self.create_storage()

class Controller:
    model = None
    
    def open_storage(self):
        self.model.open_storage()

    def create_storage(self):
        self.model.create_storage()

    def open_or_create_storage(self):
        self.model.open_or_create_storage()

class UI1:
    def open_or_create_storage(self):
        self.controller.open_or_create_storage()

class UI2:
    controller = None
    
    def open_storage(self):
        self.controller.open_storage()

    def create_storage(self):
        self.controller.create_storage()

c = Controller()
m = Model()
c.model = m

ui1 = UI1()
ui1.controller = c
print("\nUI1")
storage_exists = False
ui1.open_or_create_storage()
storage_exists = True
ui1.open_or_create_storage()

print("\nUI2")
ui2 = UI2()
ui2.controller = c
ui2.create_storage()
ui2.open_storage()
