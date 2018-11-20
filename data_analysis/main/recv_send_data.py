import datetime
from threading import Thread


class Send(Thread):
    def __init__(self, client, mysocket):
        super().__init__()
        self._client = client
        self._mysocket = mysocket

    def run(self):
        while True:
            print(datetime.datetime.now())


class Recv(Thread):
    def __init__(self, mysocket, consumer):
        super().__init__()
        self._mysocket = mysocket
        self._consumer = consumer

    def run(self):
        self._consumer.send(None)
        while True:
            data = self._mysocket.recv(3271)
            if data:
                c = self._consumer.send(data)
