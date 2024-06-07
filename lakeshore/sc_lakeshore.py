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

from instrument import Instrument
import interface as inter
import time
import json

class LS325Protocol():
    def __init__(self):
        with open('ls325commands.json') as f:
            d = json.load(f)
        self.command_list = d
    
    def get_help(self,command=None):
        if command:
            print(">>>>>> help for command: ", command, " <<<<<< ")
            print("    ", self.command_list[command])
        else:
            for key,val in self.command_list.items():
                print(">>>>>> help for command: ", key, " <<<<<< ")
                print("    ", val)

    def wrap_string(self,message):
        message+='\r\n'
        return message
    
    def decode_data(self, data):
        return(float(data.decode()))

class LS325(Instrument):
    def __init__(self,name):
        super().__init__(name)
        self.protocol = LS325Protocol()

        
    def send_command(self,command, *args):
        out_data = {}
        towrite = command + "\r\n"
        self.interface.write(towrite.encode())
        data = self.interface.readline()
        ret_val = self.protocol.decode_data(data)
        print("returned value:",  ret_val)
        #        out_data[key] = ret_val
        return ret_val
        
    def read_data(self):
        #return {"tempA":122,"tempB":123}
        list_of_command = {"TEMP_A":["KRDG?","A"], "TEMP_B":["KRDG?","B"], "HTR_1":["HTR?","1"], "HTR_2":["HTR?","2"],
                           "RANGE1":["RANGE?","1"],"RANGE2":["RANGE?","2"]}
        out_data = {}
        for key, val in list_of_command.items():
            towrite = " ".join(val) + "\r\n"
            self.interface.write(towrite.encode())
            data = self.interface.readline()
            ret_val = self.protocol.decode_data(data)
            out_data[key] = ret_val
        return out_data

        #    def get_data
    def set_(self, *args):
        print ('args ', args[0])
        to_write = [str(a) for a in args[0]]
        string_to_write = " ".join(to_write)
        self.interface.write(self.protocol.wrap_string(string_to_write).encode())
#        print(self.protocol.wrap_string(string_to_write))
#        return True
        

               
if __name__ == '__main__':
    name = "lakeshore"
    lakeshore = LS325(name)
    interface = inter.SerialInterface("LSCI,MODEL325", baudrate = 9600, bytesize=7, parity='O', stopbits=1, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False, exclusive=True)
    lakeshore.set_interface(interface)

    lakeshore.topic = 'sc/temp/lakeshore'
    if importlib.util.find_spec('libABCD'):
        import libABCD
        libABCD.init(name)
#    lakeshore.start_logging(deltat=2)
    

        #    data = lakeshore.get_data()
    
    # lakeshore.publish(lakeshore.topic, data)
               
    
