BUF_SIZE = 512

ROUTING_LIST = "routing_list.json"
DATAGRAM_PATH_NAME = 'send_route'

#IP_A = '172.18.34.118'
IP_A = '127.0.0.1'
PORT_A =12333

#IP_B = '172.18.33.216'
IP_B = '127.0.0.1'
PORT_B = 12334

#   IP_C = '172.18.35.170'
IP_C = '127.0.0.1'
PORT_C = 12335

IP_D = '127.0.0.1'
PORT_D = 12336

IP_E = '127.0.0.1'
PORT_E = 12337

PC_IP = '1'
PC_PORT = 12333

DATA_IP = '127.0.0.1'
DATA_PORT = 16000
RECV_DATA_PORT = 17000
ROUTE_PORT = 15000
RoutePort_list = {'1':15000,'2':25000,'3':35000,'4':45000,'5':55000}
ip_dict = {'1':IP_A,'2':IP_B,'3':IP_C,'4':IP_D,'5':IP_E}
port_dict = {10500:'1',11500:'1',12500:'1',20000:'2',21000:'2',30000:'3',31000:'3',40000:'4',41000:'4',42000:'4',50000:'5',51000:'5'}
name_dict = {'1':PORT_A,'2':PORT_B,'3':PORT_C,'4':PORT_D,'5':PORT_E}
#neighbour = {'4':(3,'4'),'5':(10,'5')}
neighbour = {'3':(3,'3'),'4':(10,'4'),'5':(4,'5')}
