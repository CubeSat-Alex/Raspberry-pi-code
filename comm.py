from obc import *
import json
# 
telemtry.spi.write("need" , Slave.ADCS)
data = telemtry.spi.read(Slave.TT)
# adcsData = json.loads(data)
# x=adcsData['X']
# y=adcsData['Y']
# z=adcsData['Z']
# telemtry.spi.write("need" , Slave.TT)
# data = telemtry.spi.read(Slave.TT)





# import spidev
# from ssp import *
# import time
# 
# ssp = SSP()
# spi = spidev.SpiDev()
# spi.open(0, 0)
# spi.max_speed_hz = 2000000
# 
# data = "give me GPS data" ;
# packet = ssp.data2Packet(data,Address.TT, Type.Write,1)
# 
# 
# print("Data master want to send \n"+data)
# print("packet send from master using spi\n",packet)
# for x in packet:
#     spi.xfer2([x])
# 
# spi.xfer2([0x23])
# time.sleep(0.1)
# recieved= []
# i = 0
# counter=0
# 
# print("packet recieved from slave using spi")
# 
# while True:
#     data=spi.xfer2([i])[0]
#     i+=1
#     recieved.append(data)
#     print(hex(data),end=',')
#     
#     if data == 192:
#         counter=counter+1
#         if counter==2:
#             counter=0
#             break
#    
# print('\ndata from slave')
# my_list = ssp.packet2data(recieved,1)
# # my_list = my_list.split("?")[1]
# print(my_list)
# 
# 
# # Send a null byte to check for value
# 
# data=spi.xfer2([my_list])
# 
# 
# # repeat to check for a response
# 
# rcv_byte = spi.readbytes(1)
# data_recv = rcv_byte[0]
# 
# print(send_byte)
# print(data_recv)
# 
# if (data_recv != send_byte):
# 
#     print ("Unable to communicate with Arduino "+str(data_recv))
# 
#     quit()
# else :
#     print ("able to communicate with Arduino "+str(data_recv)) 
# 
# 
# 
