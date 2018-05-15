from A.basic_A import *
import socket
import json
from struct import *

def iptoname(target_ip):
    new_dict = {v: k for k, v in ip_dict.items()}
    target_name = new_dict[target_ip]
    return target_name

def porttoname(target_port):
    new_dict = {v: k for k, v in name_dict.items()}
    target_name = new_dict[target_port]
    return target_name

def read_list(mypc_name):#trans routing_list.json to list_dict
    list_dict = {}
    with open(ROUTING_LIST,'r') as json_file:
        whole_list = json.load(json_file)
    for temp in whole_list.keys():
        if temp[0] == mypc_name:
            list_dict[temp] = whole_list[temp]
    return list_dict

def get_next_matric(list_dict,dest_name):
    next_matric_tuple = []
    for temp in list_dict.keys():
        if temp[1] == dest_name:
            next_matric_tuple = list_dict[temp]
    print("+"+next_matric_tuple[1])
    return next_matric_tuple[1]



def init_recv(src_name,data_IP,data_PORT):
    addr = (data_IP,data_PORT)
    receive_socket = socket.socket()
    receive_socket.bind(addr)
    receive_socket.listen(10)
    print("trans....")
    newSocket, destAddr = receive_socket.accept()
    print("transed", destAddr)
    while True:
        datalength = calcsize('128s12s5s')
        data = newSocket.recv(datalength)
        decode_msg,decode_src_ip,decode_dest_name = unpack('128s12s5s',data)
        msg = (decode_msg.decode('utf-8')).strip('\0')
        src_ip = (decode_src_ip.decode('utf-8')).strip('\0')
        dest_name = (decode_dest_name.decode('utf-8')).strip('\0')
        list_dict = read_list(src_name)
        next_matric_name = get_next_matric(list_dict, dest_name)
        data2 = pack('128s5s5s5s', msg.encode('utf-8'), src_name.encode('utf-8'), dest_name.encode('utf-8'),
                    next_matric_name.encode('utf-8'))
        #print("received"+str(route_PORT))
        next_IP = ip_dict[next_matric_name]
        next_PORT =RoutePort_list[next_matric_name]
        #newSocket.close()
        transport_socket = socket.socket()
        transport_socket.connect((next_IP,next_PORT))
        transport_socket.send(data2)
        transport_socket.close()

def trans_show(route_IP,route_PORT):
    addr = (route_IP,route_PORT)
    receive_socket = socket.socket()
    receive_socket.bind(addr)
    receive_socket.listen(10)
    while True:
        print("connecting....")
        newSocket,destAddr = receive_socket.accept()
        print("connected",destAddr)
        datalength = calcsize('128s5s5s5s')
        data = newSocket.recv(datalength)
        decode_msg,decode_src_name,decode_dest_name,decode_next_matric_name = unpack('128s5s5s5s',data)
        msg = (decode_msg.decode('utf-8')).strip('\0')
        src_name = (decode_next_matric_name.decode('utf-8')).strip('\0')
        dest_name = (decode_dest_name.decode('utf-8')).strip('\0')
        next_matric_name = (decode_next_matric_name.decode('utf-8')).strip('\0')

        if dest_name == next_matric_name:
            print(msg)
        else:
            print(src_name)
            list_dict = read_list(src_name)
            next_matric_name = get_next_matric(list_dict,dest_name)
            data = pack('128s5s5s5s', msg.encode('utf-8'), src_name.encode('utf-8'), dest_name.encode('utf-8'),
                        next_matric_name.encode('utf-8'))
            newSocket.close()
            transport_socket = socket.socket()
            next_IP = ip_dict[next_matric_name]
            next_PORT = RoutePort_list[next_matric_name]
            transport_socket.connect((next_IP,next_PORT))
            transport_socket.send(data)
            transport_socket.close()
if __name__ == '__main__':
    list = read_list('1')
    print(list)
    next = get_next_matric(list,'2')
    print(next)