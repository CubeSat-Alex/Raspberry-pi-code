import spidev
import time
from obc import *


spi = spidev.SpiDev()

# GPIO.setwarnings(False)
# GPIO.setup(14 , GPIO.OUT)
# GPIO.output(14 , GPIO.LOW )

spi.open(0, 0)
spi.max_speed_hz = 2000000

# Send a null byte to check for value
data = "A"
send_byte= ssp.data2Packet(data,Address.TT, Type.Read ,1)

for x in send_byte:
    spi.xfer2([x])

# data_recv=spi.xfer2([send_byte])[0]

# repeat to check for a response

# rcv_byte = spi.readbytes(1)
# data_recv = rcv_byte[0]
# spi.xfer2([0x23])
# time.sleep(0.1)
recieved= []
i = 0
counter=0
print("packet recieved from slave using spi")
# data=spi.xfer2([0x23])
time.sleep(0.1)
spi.xfer2([0x23])

while True:

    data=spi.xfer2([1])[0]
    i+=1
    recieved.append(data)
    
    print(hex(data),end=',')
   
    if data == 192:
        counter=counter+1
        if counter==2:
            counter=0
            break
print("\n")
gg = ssp.packet2data(recieved,1)
print(gg)
print("\n")
print(i)
# GPIO.output(14 , GPIO.HIGH )

# print(data_recv)




