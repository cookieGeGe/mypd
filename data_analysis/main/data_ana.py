import socket

# 导入数据库连接池
from main.recv_consumer import rec_consumer
from main.recv_send_data import Recv, Send
from main.save_data import OPMysql


def produce(c, mysocket):
    c.send(None)
    while True:
        data = mysocket.recv()
        if data:
            c = c.send(data)


if __name__ == '__main__':
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = ('192.168.1.115', 8001)
    r_c1 = rec_consumer()
    r_c2 = rec_consumer()
    mysocket.connect(address)
    t1 = Recv(mysocket, r_c1)
    t2 = Send(mysocket)
    # t1.start()
    t2.start()
    # t1.join()
    t2.join()
