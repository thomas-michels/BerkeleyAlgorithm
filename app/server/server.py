"""
    Module for Server Class
"""

from time import sleep
from typing import Any, Dict, List
from app.client import Client
import threading
from app.timer import Timer
from app.connection import SocketConnection, Connection
from app.sync import Synchronize
import socket


class Server(Client):
    """
    Server class
    """

    HOST = "localhost"
    PORT = 8000
    SOCKET = SocketConnection()
    SYNC = Synchronize()

    def __init__(self) -> None:
        self.sock = self.SOCKET.start_server_connection(self.HOST, self.PORT)

        self.time = Timer.get_time()
        self.clients: List[Connection] = []

        self.listen()

    def listen(self) -> None:
        """
        Method to listen new connections no server

        :return:
            None
        """
        self.sock.listen(5)
        print(f"Server time: {self.time}")
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: Creating new thread...")
            client, address = self.sock.accept()
            threading.Thread(target=self.listenToClient, args=(client,)).start()

    def listenToClient(self, client: socket.socket) -> None:
        """
        Method to comunicates with client

        :param:
            client: socket.socket
            adress: str

        :return:
            None
        """
        cur_thread = threading.current_thread()
        self.SOCKET.send(sock=client, message=f"ID: {cur_thread.name}")
        self.__save_client_informations(name=cur_thread.name, client=client)

        exit = False

        while not exit:
            try:
                response = self.SOCKET.recieve(sock=client)
                print(response)
                if self.SYNC.time_to_sync() and self.clients:
                    sleep(1)
                    clocks_to_adjust = self.SYNC.start_sync(
                        server_time=self.time, clients=self.clients
                    )
                    if clocks_to_adjust:
                        self.send_adjust_to_clients(clocks_to_adjust)
                        self.SYNC.unlock()
                        print("Sync Thread: Sync Completed...")

                self.SOCKET.send(sock=client, message=response)

            except:
                print(f"{cur_thread.name}: Leaving...")
                self.SOCKET.close_connection(sock=client)
                self.__remove_connection(cur_thread.name)
                exit = True

    def send_adjust_to_clients(self, times: Dict[str, Dict[str, Any]]) -> None:
        """
        Method to send clock adjust to clients

        :param:
            times: Dict[str, Dict[str, Any]]

        :return:
            None
        """
        print("Adjusting clock")
        for key in times.keys():
            client = times[key]

            if key == "server":
                self.adjust_time(client["adjust"])
                print(f"Server new time: {self.time}")

            else:
                connection = self.__search_connection_by_id(key)
                self.SOCKET.send(
                    sock=connection.get_client(),
                    message=f"clock_adjust: {client['adjust']}",
                )

                response = self.SOCKET.recieve(sock=connection.get_client())
                print(f"{key}: {response}")

    def __search_connection_by_id(self, id: str) -> Connection:
        """
        Method to search connection by id

        :param:
            id: str

        :return:
            Connection
        """
        for connection in self.clients:
            if connection.get_id() == id:
                return connection

    def __remove_connection(self, id: str) -> None:
        """
        Method to remove connection of clients list

        :param:
            id: str

        :return:
            None
        """
        self.clients.remove(self.__search_connection_by_id(id))

    def __save_client_informations(self, name, client) -> None:
        """
        Method to save client informations in Connection class

        :return:
            None
        """
        self.clients.append(Connection(id=name, client=client))
