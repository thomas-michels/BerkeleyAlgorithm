"""
    Module for Client Class
"""

from random import randint
from datetime import datetime
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
        self.id = ""
        self.time = self.__generate_random_time()
        self.start_connection()

    def start_connection(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.HOST, self.PORT))
        print(f"Cliente conectando em {self.HOST}:{self.PORT}")
        print(f"My time: {self.time}")
        try:
            while True:
                response = str(sock.recv(1024), 'ascii')
                print(response)

                if response.startswith("ID:"):
                    self.id = response.split(": ")[1]
                    message = f"{self.id}: awaiting..."
                    sock.send(bytes(message, 'ascii'))

                elif response.startswith(f"{self.id}:"):
                    message = f"{self.id}: awaiting..."
                    sock.send(bytes(message, 'ascii'))

                elif response.startswith("server_time:"):
                    message = f"time: {self.time}"
                    sock.send(bytes(message, 'ascii'))

                elif response.startswith("diff_to_server:"):

                    response = response.split(": ")[1]
                    server_time = datetime.fromisoformat(response)
                    diff = self.calculate_time_diff_to_server(server_time)
                    message = f"diff: {diff}"
                    sock.send(bytes(message, 'ascii'))

                elif response.startswith("adjust:"):
                    response = float(response.split(": ")[1])
                    self.adjust_time(response)

                    message = f"new_time: {self.time}"
                    sock.send(bytes(message, 'ascii'))

                else:
                    sock.send(b"connected")
                sleep(1)

        except Exception:
            pass
    
        finally:
            sock.close()


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
