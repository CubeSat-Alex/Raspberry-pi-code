from ssp import * 
from orders import *
from obc import *
from client import *

# print("try to connect")
# client.connect()
# print("connected")

while True:
    print("waiting for data")
    
    try : 
        packet = client.recieveData()
        if(str(packet).strip() == ""):
             raise TypeError("need to connect")
        print("data come")
        decodeThread = threading.Thread(target=decodePacket, args=(packet,))
        decodeThread.start()
    except :
        print("An error happened while reciving")
        try :
            print("try to connect")
            client.connect()
            print("connected")
            continue
        except :
            print("Already connected")

        