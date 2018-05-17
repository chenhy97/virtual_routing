from C.basic_C import *
import socket
import json
import time
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
        datalength = calcsize('128s5s12s5s')
        data = newSocket.recv(datalength)
        decode_msg,decode_cmd,decode_src_ip,decode_dest_name = unpack('128s5s12s5s',data)
        msg = (decode_msg.decode('utf-8')).strip('\0')
        cmd = (decode_cmd.decode('utf-8')).strip('\0')
        src_ip = (decode_src_ip.decode('utf-8')).strip('\0')
        dest_name = (decode_dest_name.decode('utf-8')).strip('\0')
        list_dict = read_list(src_name)
        next_matric_name = get_next_matric(list_dict, dest_name)
        data2 = pack('128s5s5s5s5s', msg.encode('utf-8'), cmd.encode('utf-8'),src_name.encode('utf-8'), dest_name.encode('utf-8'),
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
    IP = '127.0.0.1'  # client.app receive
    PORT = RECV_DATA_PORT
    while True:
        print("connecting....")
        newSocket,destAddr = receive_socket.accept()
        print("connected",destAddr)
        datalength = calcsize('128s5s5s5s5s')
        data = newSocket.recv(datalength)
        decode_msg,decode_cmd,decode_src_name,decode_dest_name,decode_next_matric_name = unpack('128s5s5s5s5s',data)
        msg = (decode_msg.decode('utf-8')).strip('\0')
        cmd = (decode_cmd.decode('utf-8')).strip('\0')
        src_name = (decode_src_name.decode('utf-8')).strip('\0')
        src_IP = ip_dict[src_name]
        src_PORT = RoutePort_list[src_name]
        dest_name = (decode_dest_name.decode('utf-8')).strip('\0')
        next_matric_name = (decode_next_matric_name.decode('utf-8')).strip('\0')
        current_name = next_matric_name
        if cmd == 'S':
            if dest_name == next_matric_name:
                print(msg)
                to_client_socket = socket.socket()
                to_client_socket.connect((IP, PORT))
                data = pack("128s5s5s", msg.encode('utf-8'),cmd.encode('utf-8'),dest_name.encode('utf-8'))
                to_client_socket.send(data)
                to_client_socket.close()
            else:
                print(next_matric_name)
                list_dict = read_list(next_matric_name)
                next_matric_name = get_next_matric(list_dict,dest_name)
                data = pack('128s5s5s5s5s', msg.encode('utf-8'),cmd.encode('utf-8'), src_name.encode('utf-8'), dest_name.encode('utf-8'),
                        next_matric_name.encode('utf-8'))
                newSocket.close()
                transport_socket = socket.socket()
                next_IP = ip_dict[next_matric_name]
                next_PORT = RoutePort_list[next_matric_name]
                transport_socket.connect((next_IP,next_PORT))
                transport_socket.send(data)
                transport_socket.close()
#            ping_socket.connect((src_IP, src_PORT))
            respose = 'R'
            res_msg = "ping back..."
            list_dict = read_list(current_name)
            print(list_dict)
            print(src_name)
            ping_socket = socket.socket()
            ping_next_matric = get_next_matric(list_dict,src_name)
            ping_next_ip = ip_dict[ping_next_matric]
            ping_next_port = RoutePort_list[ping_next_matric]
            print(ping_next_matric)
            ping_socket.connect((ping_next_ip,ping_next_port))
            ping_data = pack("128s5s5s5s5s", res_msg.encode('utf-8'),respose.encode('utf-8'), current_name.encode('utf-8'),src_name.encode('utf-8'),ping_next_matric.encode('utf-8'))
            ping_socket.send(ping_data)
            ping_socket.close()
        if cmd == 'R':
            if dest_name == next_matric_name:
                print(msg)
                to_client_socket = socket.socket()
                to_client_socket.connect((IP, PORT))
                data = pack("128s5s5s", msg.encode('utf-8'),cmd.encode('utf-8'),src_name.encode('utf-8'))
                to_client_socket.send(data)
            else:
                list_dict = read_list(next_matric_name)
                next_matric_name = get_next_matric(list_dict, dest_name)
                data = pack('128s5s5s5s5s', msg.encode('utf-8'), cmd.encode('utf-8'), src_name.encode('utf-8'),
                            dest_name.encode('utf-8'),
                            next_matric_name.encode('utf-8'))
                newSocket.close()
                transport_socket = socket.socket()
                next_IP = ip_dict[next_matric_name]
                next_PORT = RoutePort_list[next_matric_name]
                transport_socket.connect((next_IP, next_PORT))
                transport_socket.send(data)