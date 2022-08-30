from orders import *
from spi import *

class SubSytemControl:
    
    def __init__(self,telemtry):
        self.spi = telemtry.spi
    
    def telemtryOn(self):
        self.spi.write(ARD_LED_ON , Slave.TT)
        reading = self.spi.read(Slave.TT)
        if reading == "OK" :
            istelemtryOn = True

    def telemtryOff(self):
        self.spi.write(ARD_LED_OFF , Slave.TT)
        reading = self.spi.read(Slave.TT)
        if reading == "OK" :
            istelemtryOn = False
            
    def telemtryReset(self):
        self.spi.write(ARD_RESET , Slave.TT)
        reading = self.spi.read(Slave.TT)
        if reading == "OK" :
            istelemtryOn = False
        
    def testTelemtry(self):
        self.spi.write(ARD_PING , Slave.TT)
        reading = self.spi.read(Slave.TT)
        return reading == "OK"
    
    def ADCSOn(self):
        self.spi.write(ARD_LED_ON , Slave.ADCS)
        reading = self.spi.read(Slave.ADCS)
        if reading == "OK" :
            istelemtryselfOn = True

    def ADCSOff(self):
        self.spi.write(ARD_OFF , Slave.ADCS)
        reading = self.spi.read(Slave.ADCS)
        if reading == "OK" :
            istelemtryOn = False
            
    def ADCSOff(self):
        self.spi.write(ARD_RESET , Slave.ADCS)
        reading = self.spi.read(Slave.ADCS)
        if reading == "OK" :
            istelemtryOn = False
        
    def testADCS(self):
        self.spi.write(ARD_PING , Slave.ADCS)
        reading = self.spi.read(Slave.ADCS)
        return reading == "OK"
     
    def AdcsAngle(self,x,y):
        self.spi.write("{},{}".format(x,y) , Slave.ADCS)
        reading = self.spi.read(Slave.ADCS)
        return reading == "OK"
    
    
    
    
    
