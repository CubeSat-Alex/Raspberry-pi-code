import spidev
import RPi.GPIO as GPIO
import enum
from ssp import *
import time
from logs import *


class Slave(enum.Enum):
   TT = 14
   ADCS = 15

class SPI:
    telemtryBusy = False 
    adcsBusy = False 

    def __init__(self , ssp):
        self.ssp = ssp 
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 2000000
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(Slave.TT.value , GPIO.OUT)
        GPIO.setup(Slave.ADCS.value , GPIO.OUT)
      
        GPIO.output(Slave.TT.value , GPIO.HIGH)
        GPIO.output(Slave.ADCS.value , GPIO.HIGH)

    
    def write(self , data, slave):
        if slave.value == Slave.ADCS :
            print("ADCS is in onther use")
            while self.adcsBusy :
                print("." , end="")
                pass 
            print("\n----------------------------------")
            self.adcsBusy = True
        else :
            print("TT&M is in onther use")
            while self.telemtryBusy :
                print("." , end="")
                pass 
            print("\n----------------------------------")
            self.telemtryBusy = True

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
        lastValue = None
        valueCounter = 0
        while True:
            data=self.spi.xfer2([1])[0]
            i+=1
            recieved.append(data)

            if data == lastValue :
                 valueCounter =+1 
                 if valueCounter == 10 :
                    log.add(f"SPI canceled operation because repeat of {lastValue} " , LogState.Error)
                    print("SPI Canceled operation")
                    if slave == Slave.ADCS :
                        self.adcsBusy = False 
                    else :
                        self.telemtryBusy = False
                    return "ERROR"
            else :
                valueCounter = 0
            
            lastValue = data
               
            if data == 192:
                counter=counter+1
                if counter==2:
                    counter=0
                    break
        
        if slave == Slave.ADCS :
            self.adcsBusy = False 
        else :
            self.telemtryBusy = False
                
        # print('data from slave')
        data = self.ssp.packet2data(recieved,1)
        GPIO.output(slave.value , GPIO.HIGH )
        # print(data)
        return data

spi = SPI()