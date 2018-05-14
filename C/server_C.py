import socket
import threading
from C.Protocol_C import *
import time

def receive_thread(newSocket,address,route):
    count = 0
    while True:
        time.sleep(1)#睡0.5秒,与程序运行时间相加约为1秒
        data_gram = newSocket.recv(BUF_SIZE)
        if(len(data_gram) > 0):
            count = 0
            for temp in port_dict.keys():
                if address[1] == temp:
                     file_name = port_dict[temp] + '.json'
            with open(file_name,'wb') as json_obj:
                json_obj.write(data_gram)
            name = datagram(json_name = file_name)
            route.update_route(name.command,name.index)
        else:
            count = count + 1
            if count == 60:
                print('*****')
                print(address[1])
                route.shut_down(port_dict[address[1]])
                break
    print("close")
    #newSocket.close()

def receiver(route):
    HOST = '127.0.0.1'
    PORT = PC_PORT
    ADDR = (HOST,PORT)
    recSocket = socket.socket()
    #recSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    recSocket.bind(ADDR)
    recSocket.listen(10)
    while True:
        print("waiting for client")
        newSocket,destAddr = recSocket.accept()
        print("I can heiheihei")
        received_thread = threading.Thread(target = receive_thread,args = (newSocket,destAddr,route,))
        received_thread.start()

