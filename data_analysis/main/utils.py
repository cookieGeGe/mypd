import datetime
import time


def time_to_datetime(sec):
    timearray = time.localtime(sec)
    # return time.strftime('%Y-%m-%d %H:%M:%S', timearray)
    return datetime.datetime.fromtimestamp(sec)