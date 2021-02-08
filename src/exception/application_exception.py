"""
    application_exception.py
    ~~~~~~
    Created By : Pankaj Suthar
"""


class ApplicationException(Exception):
    """Application Exception Class"""

    def __init__(self, message, status_code, dev_error_message=None, error_code=None, data=None):
        """
        Constructor
        :param message: Error Message
        :param status_code: Status Code
        :param dev_error_message: Developer Error Message
        :param error_code: Developer Error Code
        :param data: Dev Error Payload
        """
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.dev_message = {
            "dev_error_message": dev_error_message,
            "data": data,
            "error_code": error_code
        }
