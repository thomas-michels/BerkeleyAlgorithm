"""
    Module for adjust time by minutes
"""

from datetime import datetime, timedelta


def adjust_time_by_minutes(time: datetime, minutes: int) -> datetime:
    """
    Method to adjust time by minutes

    :params:
        time: datetime
        minutes: int

    :return: Datetime
    """
    return time + timedelta(minutes=minutes)
