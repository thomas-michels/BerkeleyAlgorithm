"""
    Module for Berkeley Algorithm
"""

from typing import Any, Dict


class BerkeleyAlgorithm:
    """
    BerkeleyAlgorithm class
    """

    @classmethod
    def calculate(
        self, average_times: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Method to calculate clock adjust to client/server

        :param:
            average_times: Dict[str, Dict[str, Any]]

        :return:
            average_times: Dict[str, Dict[str, Any]]
        """
        diff_list = average_times["mean"]
        mean = sum(diff_list) / len(diff_list)
        average_times.pop("mean")

        for key in average_times.keys():

            diff = average_times[key]["diff"]
            average_times[key]["adjust"] = (diff * -1) + mean

        return average_times
