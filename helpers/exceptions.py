"""
Contains custom exceptions
"""
class WebException(Exception):
    """
    Custom exception for this web test framework
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
