import time
from json import loads
from struct import pack
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
            try:
                msg = redis_sub.parse_response()
                change_dict = loads(msg[2])
                ChannelNo = change_dict['ChannelNo']
                BoardCardNo = change_dict['BoardCardNo']
                PDThreshold = change_dict['PDThreshold']
                Head = b'\xe0\xe9\xe0\xe9\x62'
                Cmd = b'\x00\x03'
                BoardToPDThreshold = pack('<4s20s20s20s20sbbi',
                                          str(BoardCardNo).encode('utf-8'),  # 板卡号
                                          '255.255.255.255'.encode('utf-8'),  # IP
                                          '255.255.255.255'.encode('utf-8'),  # GateWay
                                          '255.255.255.255'.encode('utf-8'),  # Mask
                                          '255.255.255.255'.encode('utf-8'),  # ServerIP
                                          1,  # 通道数
                                          ChannelNo,  # 通道号
                                          PDThreshold)  # PD阀值
                ChangeBuffer = Head + Cmd + BoardToPDThreshold
                try_time = 1
                while try_time <= 3:
                    try:
                        self._mysocket.sendall(ChangeBuffer)
                        # print(ChangeBuffer)
                        break
                    except:
                        try_time += 1
                        time.sleep(0.5)
            except Exception as e:
                print(e)


class Recv(Thread):
    def __init__(self, mysocket, consumer):
        super().__init__()
        self._mysocket = mysocket
        self._consumer = consumer

    def run(self):
        self._consumer.send(None)
        # start_time = time.time()
        # i = 0
        while True:
            data = self._mysocket.recv(3271)
            if data:
                c = self._consumer.send(data)
                # print(current_thread().getName(), c)
                # end_time = time.time()
                # i += 1
                # if end_time - start_time >= 10:
                #     print(i / (end_time - start_time))
