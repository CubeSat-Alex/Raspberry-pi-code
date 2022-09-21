from obc import *
from client import *

leds.allOff()
# control.ADCSOn()
# control.telemtryOn()

while True :
    try:
#         print("try to connect")
        client.connect()
        break
    except :
        client.dispose()
        continue 
    
# print("connected")
leds.ledOn(Leds.Connection)

while True:
#     print("waiting for server command")    
    try : 
        packet = client.recieveData()
        if(str(packet).strip() == ""):
             raise TypeError("need to connect")
#         print("data come")
        decodeThread = threading.Thread(target=decodePacket, args=(packet,))
        decodeThread.start()
    except :
        leds.ledOf(Leds.Connection)
        print("Error while reciving")
        try :
            print("try to connect")
            client.dispose()
            client.connect()
            leds.ledOn(Leds.Connection)
            print("connected")
            continue
        except :
            print("Already connected")
            leds.ledOn(Leds.Connection)