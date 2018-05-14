from D.basic_D import *
import socket
MY_IP = '127.0.0.1'
def send_Session_layer(data_IP,data_PORT):#dest_name新设一个点
    talk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    src_ip = MY_IP
    talk.connect(data_IP,data_PORT)
    while True:
        msg = input("Route A:")
        dest_name = input("To where:")
        data = pack('128s12s5s',msg.encode('utf-8'),src_ip.encode('utf-8'),dest_name.encode('utf-8'))
        talk.send(data)

if __name__ == '__main__':
    send_Session_layer(DATA_IP,DATA_PORT)