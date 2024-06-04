import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
# directory reach
#directory = path.path(__file__).abspath() 
from instrument import Instrument

import interface as inter
import time

class RevPiProtocol():
    def __init__(self):
        pass

    def decode_data(self, data_str):
        #    [b'board:1_sensor:1_fault:168\r\n', b'board:1_sensor:2_fault:168\r\n', b'board:1_sensor:3_fault:168\r\n', b'board:1_sensor:4_fault:168\r\n', b'board:1_sensor:5_fault:168\r\n', b'board:1_sensor:6_fault:168\r\n']
        data_str = data_str.rstrip()
        split_data = data_str.split(';')        
        out_data = {}
        for d in split_data[:-1]:
            print("d", d)
            sensor = d.split("=")[0]
            meas = float(d.split("=")[1])
            out_data[sensor] = meas
        return out_data

class RevPi(Instrument):
    def __init__(self,name):
        super().__init__(name)
        self.protocol = RevPiProtocol()

    def get_data(self, *args):
        data_request = 'data_request'
        
        # Envoi de la pression demandée au client
        self.interface.server_socket.sendto(data_request.encode('utf-8'), self.interface.client_address)
        
        
        # Attente de réception de données
        print("Waiting for data...")
        data, client_address = self.interface.server_socket.recvfrom(1024)
        print("data", data)
        data = data.decode()
        dict_data = self.protocol.decode_data(data)
        print(dict_data)

if __name__ == '__main__':
    name = "revpi"
    revpi = RevPi(name)
    interface = inter.UDPSocket(name,server_ip = '134.158.153.49', client_ip='134.158.154.84', port_number=50000)
    revpi.set_interface(interface)
    data = revpi.get_data()
    
    #    revpi.interface.close()

#data = temperature_board.get_data(1,-1)

#print(data)

#while True:
#    temperat



