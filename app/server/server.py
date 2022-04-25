"""
    Module for Server Class
"""

from typing import Dict, List
from app.client import Client
from datetime import datetime


class Server(Client):
    """
    Server class
    """

    def __init__(self) -> None:
        self.time = datetime.now()
        self.client_list: List[Client] = []

    def request_client_time(self) -> None:

        times = {}

        for client in self.client_list:
            times[client.id] = {
                "time": client.time,
                "diff": client.calculate_time_diff_to_server(self.time),
                "adjust": 0,
            }

        self.__calculate_average_time_of_clients(times)

    def send_new_time(self):
        """ """

    def __calculate_average_time_of_clients(self, times: Dict[str, int]):
        """ """
