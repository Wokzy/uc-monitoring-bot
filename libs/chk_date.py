"""Библеотека, которая сравнивает текущее время на хосте с временем, которое отдает Swagger_API и БД"""

from datetime import datetime

__author__ = 'Dmitriy Minor'
__all__ = ['chk_datetime']


def chk_datetime(resp_time, max_time=1):
    """
    :param max_time: Максиммальное время расхождения между текущем временем и временем в БД
    :param resp_time: Время, которое пришло с Swagger_API или БД
    :return True - если время на хосте совпадает с resp_time
    """

    now_time = datetime.utcnow()
    if type(resp_time) is str:
        years = int(resp_time[0:4])
        mouth = int(resp_time[5:7])
        day = int(resp_time[8:10])
        hour = int(resp_time[11:13])
        minute = int(resp_time[14:16])
        second = int(resp_time[17:19])
        resp_datetime = datetime(years, mouth, day, hour, minute, second)
    else:
        resp_datetime = resp_time
    delta = now_time-resp_datetime
    if 0 <= int(delta.seconds) <= max_time:
        return True
    return False
