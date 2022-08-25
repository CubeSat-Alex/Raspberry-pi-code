from folders import *
from datetime import datetime
from spi import *
from threading import Timer


class Telemtry():
    accelerationFile = "acceleration"
    pressureFile = "pressure"
    angleFile = "angle" 
    gpsFile = "gps"
    latFile = "altitude"
    ldrFile = "ldr"
    tempretureFile = "tempreture"

    spi = SPI()

    def repeat(self,doSomeThing):
        doSomeThing()
        Timer(2,self.repeat,args=(doSomeThing,)).start()

     
    def __init__(self) :
        self.repeat(self.spi.readAll)
        


    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d/%m/%Y-%H.%M.%S,")

    def addData(self ,file, data ):
        createFolder(telemtryFolder)
        f = open( telemtryFolder + "/" + file+ ".txt" ,'a+')
        data = self.timeNow() + data
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
    
    def newAngles(self,x,y,z):
        self.addData(self.angleFile , "{},{},{}".format(x,y,z))
   
    def newLoaction(self,lat,lang):
        self.addData(self.gpsFile , "{},{},{}".format(lat,lang))
    
    def neAltitude(self,alt):
        self.addData(self.latFile , str(alt))
    
    def newlights(self,l1,l2,l3,l4):
        self.addData(self.ldrFile , "{},{},{},{}".format(l1,l2,l3,l4))
   
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

    def delete(self):
        deleteFolder(telemtryFolder)
    