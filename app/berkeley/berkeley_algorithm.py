"""
    Module for Berkeley Algorithm
"""

from typing import Dict
from app.utils import adjust_time_by_minutes


class BerkeleyAlgorithm:
    """
    BerkeleyAlgorithm class
    """

    def calculate(
        self, average_times: Dict[str, Dict[str, int]]
    ) -> Dict[str, Dict[str, int]]:
        """
        Method to calculate time for client/server

        :param:
            average_times: Dict[str, Dict[str, int]]

        :return:
            average_times: Dict[str, Dict[str, int]]
        """

        mean = self.__get_mean(average_times)

        for key in average_times.keys():
            diff = average_times[key]["diff"]
            time = average_times[key]["time"]
            average_times[key]["adjust"] = (diff * -1) + mean

        return average_times

    @staticmethod
    def __get_mean(
        average_times: Dict[str, Dict[str, int]]
    ) -> Dict[str, Dict[str, int]]:
        """
        Method to calculate mean of average_times dict

        :param:
            average_times: Dict[str, Dict[str, int]]

        :return: Dict[str, Dict[str, int]]
        """
        time_values = []

        for key in average_times.keys():
            time_values.append(average_times[key]["diff"])

        return sum(time_values) / len(time_values)
