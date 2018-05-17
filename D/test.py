from D.basic_D import *
import socket
from struct import *
import time
import multiprocessing as mp
MY_IP = '127.0.0.1'
def send_Session_layer(data_IP,data_PORT):#dest_name新设一个点
    time.sleep(2)
    talk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    src_ip = MY_IP
    addr = (data_IP,data_PORT)
    talk.connect(addr)
    while True:
        msg_far = input("Route A:")
        dest_name = input("To where:")
        cmd = "S"
        data = pack('128s5s12s5s',msg_far.encode('utf-8'),cmd.encode('utf-8'),src_ip.encode('utf-8'),dest_name.encode('utf-8'))
        talk.send(data)
        #talk.close()
def receive_Session_layer():
    receiver = socket.socket
    HOST = MY_IP
    PORT = RECV_DATA_PORT
    ADDR = (HOST, PORT)
    recSocket = socket.socket()
    # recSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    recSocket.bind(ADDR)
    recSocket.listen(10)
    while True:
        print("reciving connecting....")
        newSocket, destAddr = recSocket.accept()
        print("connected", destAddr)
        size = calcsize('128s5s5s')
        data = newSocket.recv(size)
        temp_msg,temp_cmd,temp_src_name = unpack('128s5s5s', data)
        msg = (temp_msg.decode('utf-8')).strip('\0')
        cmd = (temp_cmd.decode('utf-8')).strip('\0')
        src_name = (temp_src_name.decode('utf-8')).strip('\0')
        if cmd == "S":
            print(msg)
        if cmd == "R":
            print(src_name)
        newSocket.close()
if __name__ == '__main__':
    print('input send to send message, input receive to receive message')
    judgement = input('you want to send or receive? ')
    if judgement == 'send':
        send_Session_layer(DATA_IP,DATA_PORT)
    elif judgement == 'receive':
        receive_Session_layer()
    else:
        print('invalid input!!!')
