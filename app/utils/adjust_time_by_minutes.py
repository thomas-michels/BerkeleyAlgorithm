"""
    Module for adjust time by minutes
"""

from datetime import datetime, timedelta


def adjust_time_by_minutes(time: datetime, minutes: float) -> datetime:
    """
    Method to adjust time by minutes

    :params:
        time: datetime
        minutes: float

    :return: Datetime
    """
    return time + timedelta(minutes=minutes)
