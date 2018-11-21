import time
from threading import Thread, current_thread


class Send(Thread):
    def __init__(self, client, mysocket):
        super().__init__()
        self._client = client
        self._mysocket = mysocket

    def run(self):
        while True:
            print(time.time())


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
