from obc import *
import json 



data = { 'order' :  getTime }
data = json.loads(data)
packet = ssp.data2Packet(data)


decodePacket(packet) 

