"""
    Module for Socket Connection
"""

import socket
from app.exceptions import SendError, ReceiveError


class SocketConnection:
    """
    Class SocketConnection
    """

    SIZE: int = 1024

    @classmethod
    def send(self, sock: socket.socket, message: str) -> bool:
        try:
            sock.send(bytes(message, "ascii"))
            return True

        except Exception:
            raise SendError()

    @classmethod
    def recieve(self, sock: socket.socket) -> str:
        try:
            return str(sock.recv(self.SIZE), "ascii")

        except Exception:
            raise ReceiveError()

    @classmethod
    def start_server_connection(self, host, port) -> socket.socket:
        """
        Method to start server connection

        :param:
            host: str
            port: int

        :return:
            socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        return sock

    @classmethod
    def start_client_connection(self, host, port) -> socket.socket:
        """
        Method to start client connection

        :param:
            host: str
            port: int

        :return:
            socket
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock
