"""
    Module for Client Class
"""

from app.timer import Timer
from datetime import datetime
from app.utils import adjust_time_by_minutes
from time import sleep
from app.connection import SocketConnection


class Client:
    """
    Client class
    """

    HOST = "localhost"
    PORT = 8000

    def __init__(self) -> None:
        self.id = ""
        self.time = Timer.get_time(is_random=True)
        self.start_connection()

    def start_connection(self):
        sock = SocketConnection.start_client_connection(self.HOST, self.PORT)
        print(f"Cliente conectando em {self.HOST}:{self.PORT}")
        print(f"My time: {self.time}")
        try:
            while True:
                response = SocketConnection.recieve(sock=sock)
                print(response)

                if response.startswith("ID:"):
                    self.id = response.split(": ")[1]
                    SocketConnection.send(sock=sock, message=f"{self.id}: awaiting...")

                elif response.startswith(f"{self.id}:"):
                    SocketConnection.send(sock=sock, message=f"{self.id}: awaiting...")

                elif response.startswith("server_time:"):
                    SocketConnection.send(sock=sock, message=f"time: {self.time}")

                elif response.startswith("diff_to_server:"):

                    response = response.split(": ")[1]
                    server_time = datetime.fromisoformat(response)
                    diff = self.calculate_time_diff_to_server(server_time)

                    SocketConnection.send(sock=sock, message=f"diff: {diff}")

                elif response.startswith("adjust:"):
                    response = float(response.split(": ")[1])
                    self.adjust_time(response)

                    SocketConnection.send(sock=sock, message=f"new_time: {self.time}")

                else:
                    SocketConnection.send(sock=sock, message="Connected")

                sleep(1)

        except Exception as error:
            print(error)
    
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
            return ((server_time - self.time).seconds / 60) * -1

        return (self.time - server_time).seconds / 60

    def adjust_time(self, minutes: int) -> None:
        self.time = adjust_time_by_minutes(self.time, minutes)
