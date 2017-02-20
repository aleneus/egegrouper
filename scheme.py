# some toolkit

class WidgetFromToolkit:
    def specific_routing_for_update_data(self, data):
        print("widget: {}".format(data))

# another toolkit

class TextOutputer:
    def print_data(self, data):
        print("text outputer: {}".format(data))
        
########################################################

class Model:
    def case(self):
        return "data"


class Controller:
    model = None
    
    def set_model(self, model):
        self.model = model
    
    def set_view(self, view):
        self.view = view
        
    def case(self):
        data = self.model.case()
        self.view.show_data(data)
        

class View:
    def show_data(self, data):
        pass


class ViewGUI(View):
    widget = None

    def set_widget(self, widget):
        self.widget = widget
    
    def show_data(self, data):
        self.widget.specific_routing_for_update_data(data)
        

class ViewText(View):
    outputer = None
    
    def set_outputer(self, outputer):
        self.outputer = outputer
    
    def show_data(self, data):
        self.outputer.print_data(data)
        


m = Model()
c = Controller()
c.set_model(m)

v = ViewGUI()
w = WidgetFromToolkit()
v.set_widget(w)
c.set_view(v)
c.case()

t = TextOutputer()
v = ViewText()
v.set_outputer(t)
c.set_view(v)
c.case()
