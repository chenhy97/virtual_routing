import json
from B.basic_B import *
class Route_info:#路由表类
    def __init__(self):
        self.__map = {}
        for i in range(1,6):
            self.__map[PC_IP + str(i)] = (10000,str(i))
        self.__map[PC_IP + PC_IP] = (0,PC_IP)
        self.__save_map()

    def init_add_neighbor(self, tup, tup_data):
        self.__map[tup]= tup_data
        self.__save_map()

    def __get_map(self):
        with open(ROUTING_LIST) as json_file:
            self.__map = json.load(json_file)
    def show_map(self):
        self.__get_map()
        dict_list = []
        for temp in self.__map.keys():
            if temp[0] not in dict_list:
                dict_list.append(temp[0])
        for value in dict_list:
            value_index = {}
            for temp in self.__map.keys():
                if temp[0] == value:
                    value_index[temp] = self.__map[temp]
            print(value_index)

    def shut_down(self,dest):
        self.__get_map()
        neighbour_list = list(neighbour.keys())
        neighbour_list.remove(dest)
        delete_list = []
        for value in self.__map.keys():     #将dest从map中删除
            if value[0] == dest:
                delete_list.append(value)
        for value in delete_list:
            del self.__map[value]

        for value in self.__map.keys():                 #重置PC_IP所有权值
            if value[0] == PC_IP and value[1] in neighbour_list:
                tup = neighbour[value[1]]
                self.__map[value] = tup
            if value[0] == PC_IP and value[1] not in neighbour_list:
                if value[0] == PC_IP and value[1] == PC_IP:
                    tup = (0,value[0])
                    self.__map[value] = tup
                else :
                    tup = (10000,PC_IP)
                    self.__map[value] = tup
        for value in self.__map.keys():
            if self.__map[value][1] == dest:
                self.__map[value] = (10000,PC_IP)
        for another_temp in neighbour_list:             #更新路由表
            for value in self.__map.keys():
                if value[0] == PC_IP:
                    if self.__map[value][0] > self.__map[PC_IP + another_temp][0] + self.__map[another_temp + value[1]][0]:
                        tup = (self.__map[PC_IP + another_temp][0] + self.__map[another_temp + value[1]][0],another_temp)
                        self.__map[value] = tup
        for value in self.__map.keys():
            if value[1] == dest:
                self.__map[value] = (10000,PC_IP)
        self.__save_map()

    def __save_map(self):
        with open(ROUTING_LIST, 'w') as json_file:
            json.dump(self.__map, json_file)

    def create_index(self,dest):  # 生成一条表项   addr 是本机路由器的ip
                                    # dest是目标路由器的ip_name
        self.__get_map()
        index = {}
        for temp in self.__map.keys():
            if temp[0] == PC_IP:
                index[temp] = self.__map[temp]
        for temp in index.keys():
            if index[temp][1] == dest and temp[1] != dest:
                index[temp] = (10000,PC_IP)
        return index

    def update_route(self,cmd,index):
        self.__get_map()
        if cmd == 'LS':
            pass
        elif cmd == 'DV':
            dest = None
            for value in index.keys():
                self.__map[value] = index[value]
                dest = value[0]
            addr = PC_IP
            length = self.__map[addr + dest][0]
            for value in index.keys():
                new_length = length + self.__map[value][0]
                if new_length < self.__map[addr + value[1]][0]:
                    self.__map[addr + value[1]] = (new_length,self.__map[addr + dest][1])
            for value in self.__map.keys():
                temp = self.__map[value][1]
                if value[0] == PC_IP and temp != value[1] and temp != PC_IP:
                    if self.__map[temp + value[1]][0] == 10000:
                        self.__map[value] = (10000,PC_IP)
        else:
            print('undifiend command name!!!')
        self.__save_map()

class datagram:
    # 报文类
    def __init__(self, cmd = 0, IP = 0, PORT = 0, index = 0, json_name = ''):
        if json_name != '':
            with open(json_name,'r') as json_obj:
                json_files = json.load(json_obj)
            self.command = json_files['command']
            self.IP = json_files['IP']
            self.PORT = json_files['PORT']
            self.index = json_files['index']
        else:
            self.command = cmd
            self.IP = IP
            self.PORT = PORT
            self.index = index

    def create_datagram(self,nickname):  # 解释  接收目标地址，得到一个
        temp = {}
        temp['command'] = self.command
        temp['IP'] = self.IP
        temp['PORT'] = self.PORT
        temp['index'] = self.index
        with open(DATAGRAM_PATH_NAME+nickname+'.json','w') as json_obj:
            json.dump(temp,json_obj)


if __name__ == '__main__':
    value = Route_info()
    for i in range(1,4):
        addr = str(i)
        for j in range(1,6):
            dest = str(j)
            value.init_add_neighbor(addr + dest,(j,dest))
    value.show_map()

