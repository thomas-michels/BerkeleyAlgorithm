"""
    Module for Connections class
"""

import socket


class Connection:
    """
    Connection class
    """

    def __init__(self, id: str, client: socket.socket) -> None:
        self.__id = id
        self.__client = client

    def get_id(self) -> str:
        """
        Method to get connection id

        :return:
            str
        """
        return self.__id

    def get_client(self) -> str:
        """
        Method to get connection client

        :return:
            str
        """
        return self.__client
