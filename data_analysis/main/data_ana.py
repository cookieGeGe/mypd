import socket

# 导入数据库连接池
from main.recv_consumer import rec_consumer
from main.recv_send_data import Recv
from main.save_data import OPMysql


def produce(c, mysocket):
    c.send(None)
    while True:
        data = mysocket.recv()
        if data:
            c = c.send(data)





if __name__ == '__main__':

    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = ('127.0.0.1', 5000)
    r_c = rec_consumer()
    mysocket.connect(address)
    t1 = Recv(mysocket,)
    t1.start()
    t1.join()
