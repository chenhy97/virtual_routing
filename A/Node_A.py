from A.client_A import *
import multiprocessing as mp
from A.server_A import *
from A.msg_control import *
if __name__ == '__main__':
    route = Route_info()#初始化路由表
    for temp in neighbour.keys():#初始化路由表
        route.init_add_neighbor(PC_IP+temp,neighbour[temp])
    command = 'DV'
    p1 = mp.Process(target = sender,args = (command,route,))
    p2 = mp.Process(target = receiver,args = (route,))
    p3 = mp.Process(target = init_recv,args = (PC_IP,DATA_IP,DATA_PORT,))
    p4 = mp.Process(target = trans_show,args = (ip_dict[PC_IP],ROUTE_PORT,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()