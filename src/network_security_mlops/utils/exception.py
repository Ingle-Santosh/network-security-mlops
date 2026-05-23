import sys
from network_security_mlops.utils.logger import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        # Pass the message to the parent Exception class
        super().__init__(error_message)
        
        self.error_message = error_message
        
        # Extracting the traceback object
        _, _, exc_tb = error_details.exc_info()
        
        # Standard practice: handle cases where exc_tb might be None
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = "Unknown"
            self.file_name = "Unknown"
    
    def __str__(self):
        return f"Error occurred in python script name [{self.file_name}] line number [{self.lineno}] error message [{str(self.error_message)}]"
