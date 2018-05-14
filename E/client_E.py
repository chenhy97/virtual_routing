import socket
from E.Protocol_E import *
import threading
from E.basic_E import *
import time


FILE_NAME = "datagram.json"
def send_thread(Server_ADDR,Server_PORT,command,route,my_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', my_port))
    time.sleep(10)
    s.connect((Server_ADDR, Server_PORT))  # connect with server

    while True:
        time.sleep(5)


        new_dict = {v: k for k, v in name_dict.items()}  # 根据值获得键
        nickname = new_dict[Server_PORT]
        index_read = route.create_index(nickname)
        temp = datagram(cmd = command,IP = name_dict[PC_IP],PORT = PC_PORT,index = index_read)#生成报文
        temp.create_datagram(nickname)#生成报文类json文件
        with open(DATAGRAM_PATH_NAME+nickname+'.json',"rb") as json_obj:
            filedata = json_obj.read(BUF_SIZE)#need to define BUF_SIZE
        try:
            s.send(filedata)
        except ConnectionResetError:
            route.shut_down(nickname)
    s.shutdown(2)
    s.close()
def sender(cmd,route):
    command = cmd
    A = threading.Thread(target=send_thread,args=(IP_A,PORT_A,command,route,50000))####记得新建一个类叫做route哦
    B = threading.Thread(target=send_thread,args=(IP_B,PORT_B,command,route,51000))####记得新建一个类叫做route哦
    A.start()
    B.start()
   # D = threading.Thread(target=send_thread,args=(IP_D,PORT_D,command,route,))####记得新建一个类叫做route哦
   # E = threading.Thread(target=send_thread,args=(IP_E,PORT_E,command,route,))

   # D.start()
    #E.start()
