from glob import glob
from serial import Serial
import threading
import time
import libABCD

class Instrument:
    def __init__(self, name, **kwargs):
        self.name = name
        self.topic =''
        self.deltat = 1 
        self.stop_event= threading.Event()
        self.x = threading.Thread(target=self.continuous_log, args=(self.deltat,), daemon=True)

    def set_interface(self, interface):
        self.interface = interface

    def is_alive(self):
        return interface.is_alive()


    def get_data(self, publish=True):       
        try:
            data = self.read_data()
            if publish:
                self.publish(self.topic +'/get',data)
            return data
        except Exception as e:
            print(e)        

    def set_data(self, *args, publish=True): 
        print(args)
        try:
            validated = self.set_(args)
            if publish:
                self.publish(self.topic +'/set',args)
        except Exception as e:
            print(e)

    def continuous_log(self,deltat=1):
        while not self.stop_event.is_set():
            self.get_data()            
            time.sleep(deltat)
            
    def start_logging(self, deltat=1):
        self.stop_logging()
        self.stop_event.clear()
        print("startin with deltat = ",  deltat)
        self.x = threading.Thread(target=self.continuous_log, args=(deltat,), daemon=True)        
        self.x.start()
 
         
    def stop_logging(self):
        try:
            print("stopping thread ")
            self.stop_event.set()
            time.sleep(2)
            del self.x
        except:
            pass
    
    def publish(self,topic,data):
        libABCD.publish(topic,data)

