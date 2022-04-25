"""
    Module for Client Class
"""

from random import randint
from datetime import datetime
from uuid import uuid4
from app.utils import adjust_time_by_minutes


class Client:
    """
    Client class
    """

    def __init__(self) -> None:
        self.id = uuid4()
        self.time = self.__generate_random_time()

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
