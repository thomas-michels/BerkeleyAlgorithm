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
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: Creating new thread...")
            client, address = self.sock.accept()
            threading.Thread(target = self.listenToClient, args = (client,address)).start()

    def sync(self):
        if not self.SYNC:
            self.SYNC = True
            print("Server: Starting sync...")
            self.request_client_time()
            self.SYNC = False
            print(f"Server: SYNC COMPLETED")

        else:
            while self.SYNC:
                pass

    def listenToClient(self, client, address):
        size = 1024
        cur_thread = threading.current_thread()
        message = f"ID: {cur_thread.name}"
        client.send(bytes(message, "ascii"))
        self.__save_client_informations(cur_thread.name, client, address)

        while True:
            try:
                response = str(client.recv(size), "ascii")
                print(f"{response}")
                if self.__time_to_sync():
                    sleep(1)
                    self.sync()

                client.send(bytes(response, "ascii"))

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

    def __search_by_id(self, id: str):
        for client in self.client_list:
            if client["id"] == id:
                return client["client"]
