"""
    Module for Server Class
"""

from typing import Dict, List
from app.client import Client
from datetime import datetime
from app.berkeley import BerkeleyAlgorithm
import socket
import threading


class Server(Client):
    """
    Server class
    """

    HOST = "localhost"
    PORT = 8000

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

        self.time = datetime.now()
        self.client_list: List[Client] = []

        self.listen()

    def listen(self):
        self.sock.listen(5)
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: server listening...")
            client, address = self.sock.accept()
            client.send(b"Iniciando nova thread")
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                cur_thread = threading.current_thread()
                data = client.recv(size)
                if data:
                    response = str(data, encoding='ascii')
                    print(f"{cur_thread.name}: {response}")
                    if response == "connected":
                        client.send(b"awaiting")

                else:
                    print("disconnected")
                    raise Exception('Client disconnected')
            except:
                print(f"{cur_thread.name}: EXITING...")
                client.close()
                return False

    def request_client_time(self) -> None:

        times = {}

        print("Servidor fazendo o pedido da diferença de tempo entre os clientes")

        times["server"] = {
            "time": self.time,
            "diff": 0,
            "adjust": 0,
        }

        for client in self.client_list:
            times[client.id] = {
                "time": client.time,
                "diff": client.calculate_time_diff_to_server(self.time),
                "adjust": 0,
            }

        self.__calculate_average_time_of_clients(times)

    def send_new_time(self, times: Dict[str, int]):
        """
        Method to adjust time in all clients and server
        """
        print("Ajustando os tempos")
        for key in times:
            if key == "server":
                pass

            else:
                client = self.__search_by_id(key)
                client.adjust_time(times[key]["adjust"])

    def __search_by_id(self, id: str) -> Client:
        for client in self.client_list:
            if client.id == id:
                return client

    def __calculate_average_time_of_clients(self, times: Dict[str, int]):
        """ """

        berkeley = BerkeleyAlgorithm()

        print("Calculando o novo horário com o algoritmo de Berkeley")
        times = berkeley.calculate(times)

        self.send_new_time(times)
