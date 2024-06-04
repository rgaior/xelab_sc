from glob import glob
from serial import Serial
import time

import socket

default_baudrate = 115200
timeout=0.1
#idnstring_dict = {"pt100arduino": '*IDN?\n', "LSCI,MODEL325": '*IDN?\r\n'}
idnstring_dict = {"pt100arduino": '*IDN?\n', "LSCI,MODEL325": '*IDN?\r\n'}


class SerialInterface(Serial):
    def __init__(self, identifier, **kwargs):
        super().__init__(**kwargs)
        print(f'establishing serial connection with: {identifier}')
        if self.port is None:
            for port in glob('/dev/ttyS*'):
                try:
                    print("port = ", port)
#                    s = Serial(port, exclusive=True)
                    self.port = port
                    self.open()
                    print("port open ", port)
                    idnstring = idnstring_dict[identifier]
                    print("idnstring ", idnstring)
                    self.write(bytes(idnstring, 'utf-8'))        
                    #                    time.sleep(1.5)
                    data = self.readlines()
                    print(data[0].decode())
                    self.flush()
                    
                    if identifier in data[0].decode():
                        print("FOUND:", identifier)
                        self.port= port
                        break
                    else:
                        pass
                
#                    self.close()                    
                except  Exception as error:
                    print(error)
                    pass
        else:
            try:
                self.device = Serial(port, baudrate = baudrate, timeout=timeout)
            except:
                raise Exception('device not found at port', port)
                

class UDPSocket():
    def __init__(self, identifier, **kwargs):
        # Port and address configuration
#        server_ip, client_ip, port_number = args
        
#        port_number = 50000
#        server_ip_address ='134.158.155.84'
#        client_ip_address = '134.158.154.55'

        #    ip_address = '134.158.154.55'
        self.client_ip = kwargs['client_ip']
        self.server_ip = kwargs['server_ip']
        self.port_number = kwargs['port_number']

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (self.server_ip, self.port_number)
        self.server_socket.bind(self.server_address)
        self.client_address = (self.client_ip, self.port_number)
        
        client_address = (self.client_ip,self.port_number)
        
        print("UDP Server starting on port: ",self.port_number, " at address: ", self.server_ip)

    def close(self):
        self.server_socket.close()

if __name__ =='__main__':
    #ser = SerialInterface("pt100arduino",baudrate=115200,timeout=0.1)
    udp = UDPSocket("revpi",server_ip = '134.158.153.49', client_ip='134.158.154.84', port_number=50000)
    
