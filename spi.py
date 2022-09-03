import spidev
import RPi.GPIO as GPIO
import enum
from ssp import *
import time

class Slave(enum.Enum):
   TT = 14
   ADCS = 15

class SPI:
    ssp = SSP()
    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2000000
        GPIO.setmode(GPIO.BCM)
#         print("set to output")
        GPIO.setwarnings(False)
        GPIO.setup(Slave.TT.value , GPIO.OUT)
        GPIO.setup(Slave.ADCS.value , GPIO.OUT)
      
        GPIO.output(Slave.TT.value , GPIO.HIGH)
        GPIO.output(Slave.ADCS.value , GPIO.HIGH)

    
    def write(self , data, slave):
#         print("SEND TO SUBSYTEM {}".format(slave))
        GPIO.output(slave.value , GPIO.LOW )
        address = Address.TT if slave == Slave.TT else Address.ADCS
        packet = self.ssp.data2Packet(data,address, Type.Write,1)

#         print("Data master want to connect with to  ",slave)
#         print("packet send from master using spi\n",packet)
        for x in packet:
            self.spi.xfer2([x])
        time.sleep(1)
        self.spi.xfer2([0x23])
        
        GPIO.output(slave.value , GPIO.HIGH )
        
    def read(self , slave):
#         print("get TO SUBSYTEM {}".format(slave))
        GPIO.output(slave.value , GPIO.LOW )
        recieved= []
        i = 0
        counter=0
#         print("packet recieved from slave using spi")
        while True:
            data=self.spi.xfer2([1])[0]
            i+=1
            recieved.append(data)
            
            print(hex(data),end=',')
           
            if data == 192:
                counter=counter+1
                if counter==2:
                    counter=0
                    break
                
        print('data from slave')
        data = self.ssp.packet2data(recieved,1)
        GPIO.output(slave.value , GPIO.HIGH )
        print(data)
        return data