from folders import *
from datetime import datetime
from threading import Timer
import enum
from shared_prefrence import *

cache = Cache()
numberOfSession = cache.get("orbit")




class   LogState(enum.Enum):
   Done = "Done"
   Error = "Error"
   Loading = "Loading"


class Logs:
    def add(self , details , state):
        createFolder(logsFiles)
        f = open( logsFiles + "/log.txt" ,'a+')
        data = self.timeNow() + str(numberOfSession) + ',' + details +',' + state.value
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
        self.add(f"clearing logs storage" , LogState.Loading)
        deleteFolder(logsFiles)
        self.add(f"Logs Deleted succesfully" , LogState.Done)


log = Logs() 


def repeat(doSomeThing):
    doSomeThing()
    Timer(30,repeat,args=(doSomeThing,)).start()

def increaseOrbit():
    global numberOfSession
    numberOfSession += 1
    cache.add("orbit" ,numberOfSession )
    log.add(f"Orbit increase to {numberOfSession}" , LogState.Done)
    print(f"Number of orbit is {numberOfSession}")
    
repeat(increaseOrbit)
