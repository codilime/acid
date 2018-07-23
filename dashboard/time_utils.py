# -*- coding: utf-8 -*-
import time


def epoch_to_datetime(seconds):
    if seconds is None:
        raise TypeError
    return time.strftime("%Y-%m-%d %H:%M:%S %Z", time.gmtime(seconds))


def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def milliseconds_to_seconds(milliseconds):
    return int(milliseconds) / 1000
