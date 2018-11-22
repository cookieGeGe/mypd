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

    address_list = [('192.168.1.115', 8001), ]
    r_c_dict = {}
    for index, address in enumerate(address_list):
        r_c_dict['r_c' + str(index+1)] = rec_consumer()
        mysocket.connect(address)
        t1 = Recv(mysocket, r_c_dict['r_c' + str(index+1)])
        t2 = Send(mysocket)
        t2.start()
        t1.start()
        t1.join()
        t2.join()
