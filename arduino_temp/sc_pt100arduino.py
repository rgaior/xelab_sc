import os
import sys
import importlib.util
current = os.path.dirname(os.path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current) 
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)
from instrument import Instrument
import sc_utils 
import interface as inter
import time
import libABCD

class PT100Protocol():
    def __init__(self):
        pass

    def decode_sensor(self, data_str):
        #    [b'board:1_sensor:1_fault:168\r\n', b'board:1_sensor:2_fault:168\r\n', b'board:1_sensor:3_fault:168\r\n', b'board:1_sensor:4_fault:168\r\n', b'board:1_sensor:5_fault:168\r\n', b'board:1_sensor:6_fault:168\r\n']
        data_str = data_str.rstrip()
        split_data = data_str.split('_')
        d = split_data     
        board = int(d[0].split(":")[1])            
        sensor = int(d[1].split(":")[1])            
        meas = d[2].split(":")[0]
        temp = 0
        fault = 0
        if meas == 'temperature':
            temp = float(d[2].split(":")[1])
            tempK = sc_utils.celsius_to_kelvin(temp)
        elif meas == 'fault':
            fault = int(d[2].split(":")[1])
        print(tempK)
        return (tempK,fault)
    
    
    def decode_data(self, data, *args):
        board, sensor = args
        out_list = []
        if sensor == -1:
            for sens in range(0,6):
                out_dict = {}
                data_str = data[sens].decode('utf-8')
                (temp, fault) = self.decode_sensor(data_str)
                out_dict["board"] = board
                out_dict["sensor"] = sens
                out_dict["temp"] = temp
                out_dict["fault"] = fault
                out_list.append(out_dict)
#                out_dict[(board,sensor)] = (temp,fault)
        else:
            data_str = data[0].decode('utf-8')
            (temp, fault) = self.decode_sensor(data_str)
            out_dict["board"] = board
            out_dict["sensor"] = sens
            out_dict["temp"] = temp
            out_dict["fault"] = fault
            out_list.append(out_dict)
#            out_dict[(board,sensor)] = (temp,fault)
        return out_list

class PT100Board(Instrument):
    def __init__(self,name):
        super().__init__(name)
        self.protocol = PT100Protocol()

    def read_sensor(self, board, sensor):
        if (board > 3 or board < 1)  or (sensor > 6 or sensor < -1 or sensor ==0):
            raise Exception("incorrect number of board or sensor")
        else:
            towrite = (str(board) + ' ' + str(sensor)).encode()
            self.interface.write(towrite)
            time.sleep(1.5)
            data = self.interface.readlines()
            print(f"data = {data}")
            data = self.protocol.decode_data(data, board, sensor)
            return data
        
    def read_data(self):
        board = 1
        sensor = -1
        data = self.read_sensor(board,sensor)
        return data
if __name__ == '__main__':
    name = "pt100arduino"
    temperature_board = PT100Board(name)
    interface = inter.SerialInterface("pt100arduino", baudrate = 115200, timeout = 2, exclusive=True)
    temperature_board.set_interface(interface)
    temperature_board.topic = 'sc/temp/arduino'
    if importlib.util.find_spec('libABCD'):
        import libABCD
        libABCD.init(name)

#while True:
#    temperat



