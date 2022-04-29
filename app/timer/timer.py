"""
    Module for timer class
"""

from datetime import datetime
from random import randint
from app.utils import adjust_time_by_minutes


class Timer:
    """
    Timer class
    """

    @classmethod
    def get_time(self, is_random: bool = False) -> datetime:
        """
        Method to get time

        :return: datetime
        """
        if is_random:
            return self.__format_datetime(self.__generate_random_time())

        return self.__format_datetime(datetime.now())

    @staticmethod
    def __generate_random_time() -> datetime:
        """
        Method to generate a random time to client

        :return: Datetime
        """
        random_time_diff = randint(-1000, 1000)
        return adjust_time_by_minutes(datetime.now(), random_time_diff)

    @staticmethod
    def __format_datetime(date: datetime) -> datetime:
        """
        Method to format datetime reseting seconds

        :param:
            date: datetime

        :return: datetime
        """
        date = date.replace(second=0)
        date = date.replace(microsecond=0)
        return date
