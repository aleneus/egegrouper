from tkinter import *

class TableWidget(Frame):
    """Table widget."""
    def __init__(self, parent, names, headers, widths = []):
        Frame.__init__(self, parent)
        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.tree = ttk.Treeview(self, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.tree.yview)
        self.tree["columns"] = names[1:]
        for (name, header) in zip(names, headers):
            self.tree.heading(name, text=header)
        if len(widths) == len(names):
            for (name, width) in zip(names, widths):
                self.tree.column(name, width=width)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

    def set_handler(self, handler):
        self.tree.bind("<Double-1>", handler)
        self.tree.bind("<Return>", handler)

class StorageInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "description", "number"]
        headers = ["ID", "Name", "Description", "Num"]
        widths = [50, 100, 200, 50]
        super().__init__(parent, names, headers, widths)

class GroupInfoTable(TableWidget):
    """Table widget for stoarge info."""
    def __init__(self, parent):
        names = ["#0", "name", "age", "sex", "diagnosis"]
        headers = ["ID", "Name", "Diagnosis", "Age", "Gender"]
        super().__init__(parent, names, headers)
