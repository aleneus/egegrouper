class Widget:
    def set_data(self, data):
        print(data)

class View:
    def set_widget(self, widget):
        self.widget = widget

    def set_data(self, data):
        self.data = data

    def show_data(self):
        self.widget.set_data(self.data)

w = Widget()
v = View()
v.set_widget(w)

v.set_data("data")
v.show_data()
