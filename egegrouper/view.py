class GrouperView:
    """View in MVC. Base class."""
    
    def message(self, text):
        """Message."""
        pass
        
    def error_message(self, text):
        """Error message."""
        pass
    
    def table(self, data, headers):
        """Represent table."""
        pass

    def exam(self, e):
        """Represent examination."""
        pass

    def storage(self, exams_num, data, num_in_groups, ungrouped_num):
        """Represent information about storage."""
        pass


    
