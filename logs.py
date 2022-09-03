from folders import *
import time 
import json
from datetime import datetime


class Logs:
    def addData(self , details , state):
        createFolder(logsFiles)
        f = open( logsFiles + "/log.txt" ,'a+')
        data = self.timeNow() + ',' + details +',' + state
        f.seek(0)
        fileData = f.read(100)
        if len(fileData) > 0 :
            f.write("\n")
        f.write(data)
        f.close()
 

    def get(self):
        isExist = os.path.exists(logsFiles)
        data = ''
        if isExist:
            f = open( logsFiles + "/log.txt" ,'r')
            data = f.read() 
            f.close()
        return data

    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d/%m/%Y-%H.%M.%S,")

    def delete(self):
        deleteFolder(logsFiles)
    