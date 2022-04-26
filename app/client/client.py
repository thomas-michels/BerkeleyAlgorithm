"""
    Module for Client Class
"""

from random import randint
from datetime import datetime
from uuid import uuid4
from app.utils import adjust_time_by_minutes
import socket
from time import sleep


class Client:
    """
    Client class
    """

    HOST = "localhost"
    PORT = 8000

    def __init__(self) -> None:
        self.id = uuid4()
        self.time = self.__generate_random_time()
        self.start_connection()

    def start_connection(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        print(f"Cliente conectando em {self.HOST}:{self.PORT}")
        s.sendall(b"Conectado")
        while True:
            print(f"Hora Atual no cliente  - {self.time}")
            data = s.recv(1024)
            if data == b"get time":
                print("Servidor Solicitou Horario")
                s.sendall(bytes(str(self.time), encoding="utf-8"))

            else:
                print("Awaiting...")
                s.sendall(b"awating")

            print("#" * 50)
            sleep(1)

    def calculate_time_diff_to_server(self, server_time: datetime) -> int:
        """
        Method to calculate the diference of server time and return it in minutes

        :param:
            server_time: datetime

        :return: int
        """
        if server_time > self.time:
            return ((self.time - server_time).seconds // 60) * -1

        return (self.time - server_time).seconds // 60

    def adjust_time(self, minutes: int) -> None:
        self.time = adjust_time_by_minutes(self.time, minutes)

    @staticmethod
    def __generate_random_time() -> datetime:
        """
        Method to generate a random time to client

        :return: Datetime
        """
        random_time_diff = randint(-1000, 1000)
        return adjust_time_by_minutes(datetime.now(), random_time_diff)
