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
    SYNC = False

    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.HOST, self.PORT))

        self.time = datetime.now()
        self.client_list: List[Dict] = []

        self.listen()

    def listen(self):
        self.sock.listen(5)
        print("Starting thread for sync")
        threading.Thread(target = self.sync).start()
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: server listening...")
            client, address = self.sock.accept()
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    def sync(self):
        cur_thread = threading.current_thread()
        # lock = threading.Lock()
        while True:
            if self.__time_to_sync():
                self.SYNC = True
                # lock.acquire()
                print(f"{cur_thread.name}: SYNC TIME")
                # self.__clear_response_clients()
                sleep(1)
                self.request_client_time()
                self.SYNC = False
                # lock.release()
                print(f"{cur_thread.name}: SYNC COMPLETED")

            sleep(1)

    def listenToClient(self, client, address):
        size = 1024
        cur_thread = threading.current_thread()
        message = f"ID: {cur_thread.name}"
        client.send(bytes(message, "ascii"))
        self.__save_client_informations(cur_thread.name, client, address)

        while True:
            try:
                if not self.SYNC:
                    data = client.recv(size)
                    if data:
                        response = str(data, encoding='ascii')
                        print(f"{cur_thread.name}: {response}")
                        if not self.__time_to_sync():
                            client.send(b"awaiting")

                    # else:
                    #     client.send(b"awaiting")

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
        if self.client_list:
            for client in self.client_list:
                time = self.__request_time(client["client"])
                diff = self.__request_diff_to_server(client["client"])
                times[client["id"]] = {
                    "time": time,
                    "diff": diff,
                    "adjust": 0,
                }

            self.__calculate_average_time_of_clients(times)

    def send_new_time(self, times: Dict[str, Dict[str, int]]):
        """
        Method to adjust time in all clients and server
        """
        print("Ajustando os tempos")
        for id in times.keys():
            client = times[id]
            if id == "server":
                self.adjust_time(client["adjust"])
                print(f"Server new time: {self.time}")

            else:
                client_socket = self.__search_by_id(id)
                message = f"adjust: {client['adjust']}"
                client_socket.send(bytes(message, "ascii"))

                response = str(client_socket.recv(1024), "ascii")
                print(f"{id}: {response}")
                response = response.split(": ")[1]

    def __save_client_informations(self, name, client, address):
        self.client_list.append({
            "id": name,
            "client": client,
            "address": address
        })

    def __calculate_average_time_of_clients(self, times: Dict[str, Dict[str, int]]):
        """ """

        berkeley = BerkeleyAlgorithm()

        print("Calculando o novo horário com o algoritmo de Berkeley")
        times = berkeley.calculate(times)

        self.send_new_time(times)

    def __time_to_sync(self):
        return datetime.now().second / 20 == datetime.now().second // 20

    def __request_time(self, client):
        message = f"server_time: {self.time}"
        client.send(bytes(message, "ascii"))

        response = str(client.recv(1024), "ascii")
        response = response.split(": ")[1]
        server_time = datetime.fromisoformat(response)
        return server_time

    def __request_diff_to_server(self, client):
        message = f"diff_to_server: {self.time}"
        client.send(bytes(message, "ascii"))

        response = client.recv(1024)
        response = str(response, "ascii")
        return int(response.split(": ")[1])

    def __clear_response_clients(self):
        for client in self.client_list:
            client["client"].recv(1024)

    def __search_by_id(self, id: str):
        for client in self.client_list:
            if client["id"] == id:
                return client["client"]
