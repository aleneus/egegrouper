import readline
from collections import OrderedDict


class TextDialog:
    """Base class for text dialog."""
    def rlineinput(self, prompt, prefill=''):
        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input(prompt)
        finally:
            readline.set_startup_hook()


class FieldsTextDialog(TextDialog):
    """Text dialog for input fields values."""
    
    data_dict = None
    
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def set_data_dict(data_dict):
        self.data_dict = data_dict        
    
    def input(self):
        for key in self.data_dict:
            self.data_dict[key] = self.rlineinput(key + ': ', self.data_dict[key])
