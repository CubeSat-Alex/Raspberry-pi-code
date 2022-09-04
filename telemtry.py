from folders import *
from datetime import datetime
from spi import *
import time 
from threading import Timer
import json
from orders import *
from logs import *


 
class Telemtry():
    accelerationFile = "acceleration"
    pressureFile = "pressure"
    angleFile = "angle" 
    gpsFile = "gps"
    latFile = "altitude"
    ldrFile = "ldr"
    tempretureFile = "tempreture"

    def __init__(self,ssp):
        self.spi = SPI(ssp)
    

    def __init__(self) :
        self.repeat(self.readAll)
        
    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d/%m/%Y-%H.%M.%S,")

    def addData(self ,file, data ):
        createFolder(telemtryFolder)
        f = open( telemtryFolder + "/" + file+ ".txt" ,'a+')
        data = self.timeNow() + str(numberOfSession) + ","+ data
        f.seek(0)
        fileData = f.read(100)
        if len(fileData) > 0 :
            f.write("\n")
        f.write(data)
        f.close()

    def newAcceleration(self,acc):
        self.addData(self.accelerationFile , str(acc))

    def newPresuure(self,pressure):
        self.addData(self.pressureFile , str(pressure))
    
    def newAngles(self,a):
        self.addData(self.angleFile , "{},{},{}".format(a['X'],a['Y'],a['Z']))
   
    def newLoaction(self,location):
        self.addData(self.gpsFile , "{},{}".format(location['X'],location['Y']))
    
    def neAltitude(self,alt):
        self.addData(self.latFile , str(alt))
    
    def newlights(self,l):
        self.addData(self.ldrFile , "{},{},{},{}".format(l['LDR1'],l['LDR2'],l['LDR3'],l['LDR4']))
   
    def newTempreture(self,temp):
        self.addData(self.tempretureFile , str(temp))
    
    def get(self):
        isExist = os.path.exists(telemtryFolder)
        dict = {}
        if isExist:
            files_in_dir = os.listdir(telemtryFolder)
            for file in files_in_dir:   
                name = file.replace(".txt" , '')
                f = open(f'{telemtryFolder}/{file}' , 'r') 
                data = f.read() 
                dict[name] = data
                f.close()
        return dict
    
    def readAll(self):
        log.add("Collecting Telemtry data" , LogState.Loading)
        print("Ordering telemetry data ..... " , end="")
        try :
            ttData = self.readFrom(Slave.TT,ARD_DATA)
            adcsData = self.readFrom(Slave.ADCS ,ARD_DATA )
            self.lastData = {"TT" : ttData , "ADCS" : adcsData }
            log.add("Collecting Telemtry data" , LogState.Done)
            print("Telemtery get done")
        except :
            log.add("Collecting Telemtry data" , LogState.Error)
            return

        self.newLoaction(ttData)
        self.newlights(ttData)
        self.neAltitude(ttData['A'])
        self.newPresuure(ttData['P'])
        self.newTempreture(ttData['T'])
        
        self.newAngles(adcsData)
        self.newAcceleration(adcsData['A'])
        
    def readFrom(self,slave,order):
        time.sleep(0.1)
        self.spi.write(order,slave)
        data = self.spi.read(slave)
        data = data.replace( '":','": ').replace(',"' , ', "')
        data = json.loads(data.strip()[data.find('{'):])
        return data 
        
    def repeat(self,doSomeThing):
        doSomeThing()
        Timer(2,self.repeat,args=(doSomeThing,)).start()

    def delete(self):
        log.add(f"Telemtry Deleting " , LogState.Loading)
        deleteFolder(telemtryFolder)
        log.add(f"Telemtry Deleted succesfully" , LogState.Done)

telemtry = Telemtry(ssp)
