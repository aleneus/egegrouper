class View:
    """View in MVC. Base class"""
    data = None
    
    def set_data(self, data):
        """Set data."""
        self.data = data
    
    def show_data(self):
        """Show data."""
        pass


class ViewMessage(View):
    """Table view."""
    def set_data(self, data):
        """Set data.
        
        Parameters
        ----------
        data : str
            Message text.

        """
        super().set_data(data)

class ViewTable(View):
    """Table view."""
    def set_data(self, data):
        """Set data.
        
        Parameters
        ----------
        data : list
            Must be [rows : list of tuples] or [rows : list of tuples, headers : tuple].

        """
        super().set_data(data)

class ViewExam(View):
    def set_data(self, data):
        """Set data.
        
        Parameters
        ----------
        data : sme.Examination
           Examination instance.

        """
        super().set_data(data)
