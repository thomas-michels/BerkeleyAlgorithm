"""
    Module for synchronize class
"""

from datetime import datetime
import socket
from app.connection import Connection, SocketConnection
from typing import Any, Dict, List
from app.berkeley import BerkeleyAlgorithm


class Synchronize:
    """
    Synchronize class
    """

    SYNC = False
    SOCKET = SocketConnection()

    def unlock(self) -> None:
        """
        Method to unlock threads of sync

        :return:
            None
        """
        self.SYNC = False

    def start_sync(
        self, server_time: datetime, clients: List[Connection]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Method to start sync in one thread and lock other threads

        :param:
            server_time: datetime
            clients: List[Connection]

        :return:
            Dict[str, Dict[str, Any]]
        """
        if not self.SYNC:
            self.SYNC = True
            print("Sync Thread: Starting sync...")
            clients_infos = self.execute(server_time, clients)
            return clients_infos

        else:
            while self.SYNC:
                pass

    @classmethod
    def time_to_sync(self) -> bool:
        """
        Method to check if is time to sync clocks

        Sync is each 20 seconds

        :return:
            Bool
        """
        return datetime.now().second / 20 == datetime.now().second // 20

    def execute(
        self, server_time: datetime, clients: List[Connection]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Method to execute sync in all clocks

        :param:
            server_time: datetime
            clients: List[Connection]

        :return:
            Dict[str, Dict[str, Any]]
        """

        print("Server doing requests for all clients")
        clients_infos = self.__get_clients_infos(
            server_time=server_time, clients=clients
        )

        return self.__calculate_clock_adjust(times=clients_infos)

    def __get_clients_infos(
        self, server_time: datetime, clients: List[Connection]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Method to get infos to execute sync

        :param:
            server_time: datetime
            client: socket.socket

        :return:
            Dict[str, Dict[str, Any]]
        """
        clients_infos = {
            "mean": [0],
            "server": {
                "diff": 0,
                "adjust": 0,
            },
        }

        for connection in clients:
            diff = self.__request_clock_diff_to_server(
                server_time=server_time, client=connection.get_client()
            )

            clients_infos[connection.get_id()] = {
                "diff": diff,
                "adjust": 0,
            }

            clients_infos["mean"].append(diff)

        return clients_infos

    def __request_clock_diff_to_server(
        self, server_time: datetime, client: socket.socket
    ):
        """
        Method to request clock diff to server

        :param:
            server_time: datetime
            client: socket.socket

        :return:
            datetime
        """
        self.SOCKET.send(sock=client, message=f"clock_diff: {server_time}")

        response = self.SOCKET.recieve(sock=client)
        return float(response.split(": ")[1])

    def __calculate_clock_adjust(
        self, times: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Method to calculate clock adjust with Berkeley Algorithm

        times: Dict[str, Dict[str, Any]]

        :return:
            Dict[str, Dict[str, Any]]
        """
        print("Calculating clock adjust")
        times = BerkeleyAlgorithm.calculate(average_times=times)
        return times
