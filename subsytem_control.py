from orders import *
from spi import *
from logs import *

class SubSytemControl:
        
    def telemtryOn(self):
        log.add("turning TT&M subsytem on" , LogState.Loading)
        spi.write(ARD_LED_ON , Slave.TT)
        reading = spi.read(Slave.TT)
        if(reading == "ok"):
            log.add("turning TT&M subsytem on" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem on with {reading}" , LogState.Error)
        return reading == "OK"

    def telemtryOff(self):
        log.add("turning TT&M subsytem off" , LogState.Loading)
        spi.write(ARD_LED_OFF , Slave.TT)
        reading = spi.read(Slave.TT)
        if(reading == "ok"):
            log.add("turning TT&M subsytem off" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem off with {reading}" , LogState.Error)
        return reading == "OK" 
            
    def telemtryReset(self):
        log.add("Reset TT&M subsytem" , LogState.Loading)
        spi.write(ARD_RESET , Slave.TT)
        reading = spi.read(Slave.TT)
        if(reading == "ok"):
            log.add("Reset TT&M subsytem" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem with {reading}" , LogState.Error)
        return reading == "OK" 
        
    def testTelemtry(self):
        log.add("Sending ping to TT&M subsytem" , LogState.Loading)
        spi.write(ARD_PING , Slave.TT)
        reading = spi.read(Slave.TT)
        if(reading == "ok"):
            log.add("TT&M Subsytem Acknolgment recived succesfully" , LogState.Done)
        else :
            log.add(f"TT&M Subsytem Acknolgment dosdn't recived with {reading}" , LogState.Error)
        return reading == "OK"
    
    def ADCSOn(self):
        log.add("turning ADCS subsytem on" , LogState.Loading)
        spi.write(ARD_LED_ON , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "ok"):
            log.add("turning ADCS subsytem on" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem on with {reading}" , LogState.Error)
        return reading == "OK" 

    def ADCSOff(self):
        log.add("turning ADCS subsytem off" , LogState.Loading)
        spi.write(ARD_LED_OFF , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "ok"):
            log.add("turning ADCS subsytem off" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem off with {reading}" , LogState.Error)
        return reading == "OK" 
            
    def testADCS(self):
        log.add("Sending ping to ADCS subsytem" , LogState.Loading)
        spi.write(ARD_PING , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "ok"):
            log.add("ADCS Subsytem Acknolgment recived succesfully" , LogState.Done)
        else :
            log.add(f"ADCS Subsytem Acknolgment dosdn't recived with {reading}" , LogState.Error)
        return reading == "OK"
        
    def adcsReset(self):
        log.add("Reset ADCS subsytem " , LogState.Loading)
        spi.write(ARD_RESET , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "ok"):
            log.add("Reset DCS subsytem" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem with {reading}" , LogState.Error)
        return reading == "OK" 
        
    def AdcsAngle(self,x,y):
        log.add(f"Set ADCS angle to {x},{y} " , LogState.Loading)
        spi.write("{},{}".format(x,y) , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "ok"):
            log.add(f"ADCS angle to {x},{y} set sucessfully" , LogState.Done)
        else :
            log.add(f"ADCS angle to {x},{y} doesn't set with {reading}" , LogState.Error)
        return reading == "OK"

control = SubSytemControl()