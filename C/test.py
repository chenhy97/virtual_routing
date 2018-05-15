from C.basic_C import *
import socket
from struct import *
MY_IP = '127.0.0.1'
def send_Session_layer(data_IP,data_PORT):#dest_name新设一个点
    talk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    src_ip = MY_IP
    addr = (data_IP,data_PORT)
    talk.connect(addr)
    while True:
        msg = input("Route C:")
        dest_name = input("To where:")
        data = pack('128s12s5s',msg.encode('utf-8'),src_ip.encode('utf-8'),dest_name.encode('utf-8'))
        talk.send(data)

if __name__ == '__main__':
    send_Session_layer(DATA_IP,DATA_PORT)