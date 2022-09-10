from orders import *
from spi import *
from logs import *
from shared_prefrence import *


class SubSytemControl:
    x = cache.get('x')
    y = cache.get('y')
    TTOn = cache.get('TT')
    ADOn = cache.get('ADCS')
        
    def telemtryOn(self):
        log.add("turning TT&M subsytem on" , LogState.Loading)
        spi.write(ARD_LED_ON , Slave.TT)
        reading = spi.read(Slave.TT).strip()
        print(reading)
        if(reading == "Ok"):
            TTOn = 1
            cache.add('TT' , 1 )
            log.add("turning TT&M subsytem on" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem on with {reading}" , LogState.Error)
        return reading == "OK"

    def telemtryOff(self):
        log.add("turning TT&M subsytem off" , LogState.Loading)
        spi.write(ARD_LED_OFF , Slave.TT)
        reading = spi.read(Slave.TT).strip()
        print(reading)
        if(reading == "Ok"):
            TTOn = 0
            cache.add('TT' , 0 )
            log.add("turning TT&M subsytem off" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem off with {reading}" , LogState.Error)
        return reading == "OK" 
            
    def telemtryReset(self):
        log.add("Reset TT&M subsytem" , LogState.Loading)
        spi.write(ARD_RESET , Slave.TT)
        reading = spi.read(Slave.TT).strip()
        if(reading == "Ok"):
            TTOn = 0
            cache.add('TT' , 0 )
            log.add("Reset TT&M subsytem" , LogState.Done)
        else :
            log.add(f"turning TT&M subsytem with {reading}" , LogState.Error)
        return reading == "OK" 
        
    def testTelemtry(self):
        log.add("Sending ping to TT&M subsytem" , LogState.Loading)
        spi.write(ARD_PING , Slave.TT)
        reading = spi.read(Slave.TT).strip()
        if(reading == "Ok"):
            log.add("TT&M Subsytem Acknolgment recived succesfully" , LogState.Done)
        else :
            log.add(f"TT&M Subsytem Acknolgment dosdn't recived with {reading}" , LogState.Error)
        return reading == "OK"
    
    def ADCSOn(self):
        log.add("turning ADCS subsytem on" , LogState.Loading)
        spi.write(ARD_LED_ON , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        print(reading)
        if(reading == "Ok"):
            ADOn = 1
            ADOn = cache.add('ADCS' , 1)
            log.add("turning ADCS subsytem on" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem on with {reading}" , LogState.Error)
        return reading == "OK" 

    def ADCSOff(self):
        log.add("turning ADCS subsytem off" , LogState.Loading)
        spi.write(ARD_LED_OFF , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        print(reading)
        if(reading == "OK"):
            ADOn = 0
            ADOn = cache.add('ADCS' , 0)
            log.add("turning ADCS subsytem off" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem off with {reading}" , LogState.Error)
        return reading == "OK" 
            
    def testADCS(self):
        log.add("Sending ping to ADCS subsytem" , LogState.Loading)
        spi.write(ARD_PING , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "Ok"):
            ADOn = 0
            ADOn = cache.add('ADCS' , 0)
            log.add("ADCS Subsytem Acknolgment recived succesfully" , LogState.Done)
        else :
            log.add(f"ADCS Subsytem Acknolgment dosdn't recived with {reading}" , LogState.Error)
        return reading == "OK"
        
    def adcsReset(self):
        log.add("Reset ADCS subsytem " , LogState.Loading)
        spi.write(ARD_RESET , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        if(reading == "Ok"):
            log.add("Reset DCS subsytem" , LogState.Done)
        else :
            log.add(f"turning ADCS subsytem with {reading}" , LogState.Error)
        return reading == "OK" 
        
    def AdcsAngle(self,x,y):
        log.add(f"Set ADCS angle to {x},{y} " , LogState.Loading)
        if int(x)==self.x and int(y)== self.y :
            return
        
        spi.write("{},{}".format(int(x),int(y)) , Slave.ADCS)
        reading = spi.read(Slave.ADCS)
        print(reading)
        if(reading == "OK"):
            self.x  = int(x)
            self.y = int(y)
            cache.add('x' , self.x )
            cache.add('y',self.y )
            log.add(f"ADCS angle to {x},{y} set sucessfully" , LogState.Done)
        else :
            log.add(f"ADCS angle to {x},{y} doesn't set with {reading}" , LogState.Error)
        return reading == "OK"

control = SubSytemControl()