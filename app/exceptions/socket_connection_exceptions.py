"""
    Module for all expetions for SocketConnection
"""


class SendError(Exception):
    """
    Raised when occur error on send message
    """


class ReceiveError(Exception):
    """
    Raised when occur error on receive message
    """
