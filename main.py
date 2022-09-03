from ssp import * 
from orders import *
from obc import *
from client import *

leds.allOn()
print("try to connect")
client.connect()
print("connected")
leds.ledOn(Leds.GREEN)

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
        leds.ledOf(Leds.GREEN)
        print("Error while reciving")
        try :
            print("try to connect")
            client.connect()
            leds.ledOn(Leds.GREEN)
            print("connected")
            continue
        except :
            print("Already connected")
            leds.ledOn(Leds.GREEN)

    