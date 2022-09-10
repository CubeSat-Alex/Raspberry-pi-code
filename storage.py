import os
from folders import *

GIGA = 1000000000

maxImages = 5*GIGA
maxVideos = 10*GIGA
maxLogs = 3*GIGA
maxTelemtry = 2*GIGA


class Storage :

    def getSize(self,start_path = '.'):
        total_size = 0
        for dirpath, _, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
        return total_size


    def getStorage(self):
        return  {
            "Images" : self.getSize(imageFolder) ,
            "Videos" : self.getSize(videosFolder),
            "Telemtry" : self.getSize(telemtryFolder) ,
            "Logs" : self.getSize(logsFiles)
            }
    
storage = Storage()