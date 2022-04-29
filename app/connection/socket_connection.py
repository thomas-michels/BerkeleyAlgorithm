"""
    Module for Socket Connection
"""

import socket
from app.exceptions import SendError, ReceiveError, SocketConnectionError


class SocketConnection:
    """
    Class SocketConnection
    """

    SIZE: int = 1024

    @classmethod
    def send(self, sock: socket.socket, message: str) -> None:
        """
        Method to send a message to socket

        Raises SendError if occur error in send

        :param:
            sock: socket.socket
            message: str

        :return: None
        """
        try:
            sock.send(bytes(message, "ascii"))

        except Exception:
            raise SendError()

    @classmethod
    def recieve(self, sock: socket.socket) -> str:
        """
        Method to receive a message of socket

        Raises ReceiveError if occur error in receive

        :param:
            sock: socket.socket

        :return: str
        """
        try:
            return str(sock.recv(self.SIZE), "ascii")

        except Exception:
            raise ReceiveError()

    @classmethod
    def start_server_connection(self, host, port) -> socket.socket:
        """
        Method to start server connection

        Raises SocketConnectionError if occur error in start connetion

        :param:
            host: str
            port: int

        :return:
            socket
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            return sock

        except Exception:
            raise SocketConnectionError()

    @classmethod
    def start_client_connection(self, host, port) -> socket.socket:
        """
        Method to start client connection

        Raises SocketConnectionError if occur error in start connetion

        :param:
            host: str
            port: int

        :return:
            socket
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            return sock

        except Exception:
            raise SocketConnectionError()

    def close_connection(self, sock: socket.socket) -> None:
        """
        Method to close socket connection

        :param:
            sock: socket.socket

        :return:
            None
        """
        sock.close()
