import time
from json import loads
from threading import Thread, current_thread

from main.redishelper import RedisHelper


class Send(Thread):
    def __init__(self, mysocket):
        super().__init__()
        self._mysocket = mysocket

    def run(self):
        redis_obj = RedisHelper()
        redis_sub = redis_obj.subscribe()
        while True:
            msg = redis_sub.parse_response()
            a = loads(msg[2])
            print(a['hello'])


class Recv(Thread):
    def __init__(self, mysocket, consumer):
        super().__init__()
        self._mysocket = mysocket
        self._consumer = consumer

    def run(self):
        self._consumer.send(None)
        start_time = time.time()
        i = 0
        while True:
            data = self._mysocket.recv(3271)
            if data:
                c = self._consumer.send(data)
                print(current_thread().getName(), c)
                end_time = time.time()
                i += 1
                if end_time - start_time >= 10:
                    print(i / (end_time - start_time))
