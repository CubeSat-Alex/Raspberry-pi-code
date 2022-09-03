import enum
from crc import CrcCalculator, Crc16



class   Address(enum.Enum):
   GS = 0x00
   OBC = 0X01
   ADCS = 0X10
   TT = 0X11 

class   Type(enum.Enum):
   Read = 0x06
   Write = 0X07
   ACK = 0X02
   Ping = 0X00 

class SSP():
    SRC = Address.OBC 
    fund = 0xc0
    crc_calculator = CrcCalculator(Crc16.CCITT)

    def data2Packet(self,data , DEST , Type , ard = 0):
        packet = [(ord(character)) for character in data] 
        packet = [DEST.value , self.SRC.value  , Type.value  ] + packet
        checksum = (self.crc_calculator.calculate_checksum(bytes(packet)))
        high , low = (checksum >> 8, checksum & 0xFF)
        packet =  packet + [ low , high ]
        packet = self.replaceFundinData(packet)
        packet = [self.fund] + packet + [self.fund]
        if(ard == 0):
            packet = [hex(x) for x in packet]
        return packet
    
    def packet2data(self,packet, ard = 0):
        data = packet 
        if(ard == 0):
            data = [int(x,16) for x in packet]
        data = data[1:-1]
        data = self.replaceFundinPacket(data)
        high = data[-1] << 8 
        low = data[-2]
        checksum = low + high
        data = data[0:-2]
        exceptCheckSum = (self.crc_calculator.calculate_checksum(bytes(data)))

        if True :#checksum ==  exceptCheckSum and data[1] == self.SRC.value:
            data = data[3:]
            return ''.join(chr(i) for i in data)

    def replaceFundinData(self,data):
        # check if 0xdb 0xdc replace with 0xdb 0xdd
        indexes = [index for (index, item) in enumerate(data) if item == 0xdb ]
        for i in indexes :
            try:            
                if(data[i+1] == 0xdc):
                        data[i+1] = 0xdd
            except :
                pass 

        # check if 0xc0 replace it with 0xdb 0xdc 
        indexes = [index for (index, item) in enumerate(data) if item == 0xc0 ]
        for i in indexes :
            try :
                data[i] = 0xdb 
                data.insert(i+1, 0xdc)
            except :
                pass
        return data 

    def replaceFundinPacket(self,packet):
         # check if 0xc0 replace it with 0xdb 0xdc 
        indexes = [index for (index, item) in enumerate(packet) if item == 0xdb ]
        for i in indexes :
            try :
                if(packet[i+1] == 0xdc):
                    packet[i] = 0xc0
                    del packet[i+1]
            except :
                pass 
        # check if 0xdb 0xdd replace with 0xdb 0xdc
        indexes = [index for (index, item) in enumerate(packet) if item == 0xdb ]
        for i in indexes :
            try :
                if(packet[i+1] == 0xdd):
                    packet[i+1] = 0xdc
            except :
                    pass
        return packet 

        
    

    