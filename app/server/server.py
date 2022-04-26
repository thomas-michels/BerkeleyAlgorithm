"""
    Module for Server Class
"""

from time import sleep
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
        self.client_list: List[Dict] = []

        self.listen()

    def listen(self):
        self.sock.listen(5)
        print("Creating thread for sync")
        threading.Thread(target = self.sync).start()
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: server listening...")
            client, address = self.sock.accept()
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    def sync(self):
        cur_thread = threading.current_thread()
        while True:
            if self.__time_to_sync():
                print(f"{cur_thread.name}: SYNC TIME")

            sleep(1)

    def listenToClient(self, client, address):
        size = 1024
        cur_thread = threading.current_thread()
        message = f"ID: {cur_thread.name}"
        client.send(bytes(message, "ascii"))
        self.__save_client_informations(cur_thread.name, client, address)

        while True:
            try:
                data = client.recv(size)
                if data:
                    response = str(data, encoding='ascii')
                    print(f"{cur_thread.name}: {response}")
                    if self.__time_to_sync():
                        message = f"server_time: {self.time}"
                        client.send(bytes(message, "ascii"))

                    else:
                        # if response.startswith("time:"):
                        #     response

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

    def __save_client_informations(self, name, client, address):
        self.client_list.append({
            "id": name,
            "client": client,
            "address": address
        })

    def __calculate_average_time_of_clients(self, times: Dict[str, int]):
        """ """

        berkeley = BerkeleyAlgorithm()

        print("Calculando o novo horário com o algoritmo de Berkeley")
        times = berkeley.calculate(times)

        self.send_new_time(times)

    def __time_to_sync(self):
        return datetime.now().second / 10 == datetime.now().second // 10
