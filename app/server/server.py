# """
#     Module for Server Class
# """

# from typing import Dict, List
# from app.client import Client
# from datetime import datetime
# from app.berkeley import BerkeleyAlgorithm
# import socketserver
# from threading import Thread


# class Server(Client, socketserver.BaseRequestHandler):
#     """
#     Server class
#     """

#     HOST = "localhost"
#     PORT = 8000

#     def __init__(self) -> None:
#         self.time = datetime.now()
#         self.client_list: List[Client] = []

#     def handle(self):
#         """
#         """
#         # def start_comunication():
#         print(f'Conexões: {self.client_address}')
#         self.data = self.request.recv(1024)
#         print(f"{self.data}")
#         self.request.sendall(b"get time")

#         # Thread(start_comunication()).start()

#     def request_client_time(self) -> None:

#         times = {}

#         print("Servidor fazendo o pedido da diferença de tempo entre os clientes")

#         times["server"] = {
#             "time": self.time,
#             "diff": 0,
#             "adjust": 0,
#         }

#         for client in self.client_list:
#             times[client.id] = {
#                 "time": client.time,
#                 "diff": client.calculate_time_diff_to_server(self.time),
#                 "adjust": 0,
#             }

#         self.__calculate_average_time_of_clients(times)

#     def send_new_time(self, times: Dict[str, int]):
#         """
#         Method to adjust time in all clients and server
#         """
#         print("Ajustando os tempos")
#         for key in times:
#             if key == "server":
#                 pass

#             else:
#                 client = self.__search_by_id(key)
#                 client.adjust_time(times[key]["adjust"])

#     def __search_by_id(self, id: str) -> Client:
#         for client in self.client_list:
#             if client.id == id:
#                 return client

#     def __calculate_average_time_of_clients(self, times: Dict[str, int]):
#         """ """

#         berkeley = BerkeleyAlgorithm()

#         print("Calculando o novo horário com o algoritmo de Berkeley")
#         times = berkeley.calculate(times)

#         self.send_new_time(times)

import socketserver
from threading import Thread
from time import sleep

class ProcessThread(Thread):
    """
    Process Thread class
    """

    def __init__(self, time_await, function):
        Thread.__init__(self)
        self.time_await = time_await
        self.function = function

    def run(self):
        while True:
            sleep(self.time_await)
            self.function()


class Server(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    threads = []

    def handle(self):
        thread = ProcessThread(1, self.stablish_connection)
        thread.start()
        self.threads.append(thread)

        self.run_and_join_threads()

    def run_and_join_threads(self):
        for thread in self.threads:
            thread.join()

    def stablish_connection(self):
        self.data = self.request.recv(1024).strip()
        # print("{} wrote:".format(self.client_address[0]))
        print(f"Conexoes: {self.client_address}")
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(b"get time")
        self.data = self.request.recv(1024).strip()
        print(self.data)
