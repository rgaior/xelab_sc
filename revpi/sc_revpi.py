import sys
import os
import importlib.util
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

#    def get_data(self, *args):
    def read_data(self, *args):
        data_request = 'data_request'
        
        # Envoi de la pression demandée au client
        self.interface.server_socket.sendto(data_request.encode('utf-8'), self.interface.client_address)



        # Réception du nombre de chaînes de caractères à recevoir
        num_strings_data, client_address = self.interface.server_socket.recvfrom(1024)  # Recevoir les données
        num_strings = int(num_strings_data.decode('utf-8'))  # Convertir en entier
        print(f"Nombre de chaînes de caractères à recevoir: {num_strings}")
        
        for _ in range(num_strings):
            data, client_address = self.interface.server_socket.recvfrom(1024)            
            print("data", data)
            data = data.decode('utf_8')   
            dict_data = self.protocol.decode_data(data)
            print(dict_data)

        return dict_data

if __name__ == '__main__':
    name = "revpi"
    revpi = RevPi(name)
    interface = inter.UDPSocket(name,server_ip = '134.158.155.84', client_ip='134.158.154.84', port_number=50000)
    revpi.set_interface(interface)
    revpi.topic = 'sc/gaz/revpi'
    if importlib.util.find_spec('libABCD'):
        import libABCD
        libABCD.init(name)


        
#data = temperature_board.get_data(1,-1)

#print(data)

#while True:
#    temperat



