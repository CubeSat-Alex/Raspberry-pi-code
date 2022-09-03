import time as time
import threading , json
from ssp import * 
from pyload import *
from orders import *
from client import *
from telemtry  import *
from logs import *
from datetime import datetime
import os
from data import *

ssp = SSP()
telemtry = Telemtry()
control = SubSytemControl(telemtry)
payload = Pyload(control)
client = Client()
logs = Logs()
leds = ModesLed()

isTelemetryOn = False 
isAdcsOn = False
isCameraOn = False

def sendDtring(data):
    jsonData = json.dumps(data)
    print( "Data to sent "+ jsonData)
    packet = ssp.data2Packet(jsonData, Address.GS , Type.Read )
#     print("SSP Packet {}".format(packet))
    packet = ','.join([str(elem) for elem in  packet])
    lenght = len(packet)
    start = 0 

    while True :
        end = start + 4096 
        end = lenght if end >lenght else end
        sended = packet[ start : end ]
        client.senData(sended)
        start = end

        if( end >= lenght):
            print("endded")
            client.senData("end of data")
            break 

def sendImages():
    path = imageFolder
    isExist = os.path.exists(path)
    if isExist:
        files_in_dir = os.listdir(path)
        imageLenght = len(files_in_dir)
        data = {"imageLenght" : imageLenght  , "imagesNames" : files_in_dir}
        sendDtring(data)
        time.sleep(1)
        for file in files_in_dir:   
            client.sendImage(f'{path}/{file}')
            time.sleep(0.5)

def sendVideos():
    path = videosFolder
    isExist = os.path.exists(path)
    if isExist:
        files_in_dir = os.listdir(path)
        videosLenght = len(files_in_dir)
        data = {"videosLenght" : videosLenght  , "VideosNames" : files_in_dir}
        sendDtring(data)
        time.sleep(1)
        for file in files_in_dir:   
            client.sendVideo(f'{path}/{file}')
            time.sleep(0.5)

def decodePacket(packet):
    packet = packet.split(',')
#     print("Packet Recived : {}".format(packet) )
    recived = ssp.packet2data(packet)
#     print(recived)

    recivedJson = json.loads(recived)
    print("Json Data Recived : {}".format(recivedJson) )
    command = recivedJson['order']

    if command == getImageNow :
        print("Order is to get image now and send it")
        start = datetime.now()
        frame = payload.takeImage()
        print('Time after taking picture: {}'.format(datetime.now()- start))
        try :
            print("Image taked succesfully , sending")
            client.sendFrame(frame)
            print('Time after sending picture: {}'.format(datetime.now() - start))
        except :
            print("An error happened while takeing the photo")
    elif command == getStream :
        print('Start stream at: {}'.format(datetime.now()))
        print("order is to get Stream Now")
        client.stream("http://192.168.43.1:6677/videofeed?username=CCJDMAFKB&password=")
    elif command == stopStream : 
        print("order is to stop Stream Now")
        client.stopStream()
    elif command == getTime :
        print("order is get time now")
        now = datetime.now()
        data = now.strftime("%d-%m-%Y %H:%M:%S")
        print("Time now in RPI is ",data)
        sendDtring(data)
    elif command == setTime :
        print("order is set time now")
        wanted_time = recivedJson['args']['time'] 
        dateTime = datetime.strptime(wanted_time, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        print("Requested time is " , dateTime)
#         os.system("sudo systemctl stop systemd-timesyncd")
#         os.system("sudo systemctl disable systemd-timesyncd")
        print(os.system("sudo date -s '{}'".format(dateTime)))
#         print(datetime.now())
    elif command ==  setNextSession :
        print("order is set next session")
        start = recivedJson['args']['start'] 
        startTime = datetime.strptime(start, '%d-%m-%Y %H:%M:%S')
        end = recivedJson['args']['end'] 
        endTime = datetime.strptime(end, '%d-%m-%Y %H:%M:%S')
        now = datetime.now()
        toStart = (startTime - now).total_seconds()
        duration = (endTime - now).total_seconds()

        def nextSession(duration):
            print("next session is now and end after",duration)
            def closeSession():
                print("session closed ") 
            threading.Timer(duration, closeSession).start()

        threading.Timer(toStart, nextSession ,args = (duration,)).start()
    elif command == subsytemControl :
        print("Subsytem control")
        args = recivedJson['args']
        print("arguments")
        subsytem = args['sys']
        order = args['command']
        if order == "ON" : 
            if subsytem == "ADCS" :
                control.ADCSOn()
            else :
                control.telemtryOn()
        elif order == "OFF" :
            if subsytem == "ADCS" :
                control.ADCSOff()
            else :
                control.telemtryOff()
        elif order == "RESET" :
            if subsytem == "ADCS" :
                control.adcsReset()
            else :
                control.telemtryReset()
        elif order == "LIVE" :
            if subsytem == "ADCS" :
                control.testADCS()
            else :
                control.testTelemtry()
        elif order == "angle" :
            print(f"X {args['X']} , Y{args['Y']} ")
            control.AdcsAngle(args['X'] , args ['Y'])
    elif command == subsytemStatus :
        sys = recivedJson['args']['sys']
        if sys == "ADCS" :
            control.testADCS()
        else :
            control.testTelemtry()
    elif command == directTelemetry :
        print("Direct telemtry orderd")
        sendDtring(telemtry.lastData)
    elif command == getTelemetry :
        print("order is to get Telemetry now")
        data = telemtry.get()
        sendDtring(data)
    elif command == deleteTelemetry :
        print("order is to delete telemetry")
        telemtry.delete()
    elif command == getLogs :
        print("order is to get Logs now")
        data = logs.get()
        sendDtring(data)
    elif command == deleteLogs :
        print("order is to delete logs")
        logs.delete()
    elif command == getImages :
        print("order is to get images now")
        sendImages()
    elif command == getVideos :
        print("order is to get videos Now")
        sendVideos()
    elif command == deleteImages :
        print("order is to delete videos Now")
        payload.deleteImages()
    elif command == deleteVideos :
        print("order is to delete videos Now")
        payload.deleteVideos()
    elif command == getVideoAt :
        duration = recivedJson['args']['duration']
        time =  recivedJson['args']['time']
        mission =  recivedJson['args']['mission']
        x =  recivedJson['args']['X']
        y =  recivedJson['args']['Y']
        print('order is to take video for {}'.format(duration)) 
        payload.takeViderAt(time , duration,x,y , mission)
    elif command == getImageAt :
        time =  recivedJson['args']['time']
        mission =  recivedJson['args']['mission']
        x =  recivedJson['args']['X']
        y =  recivedJson['args']['Y']
        print('order is to take image at {}'.format(time)) 
        payload.takeImageAt(time,x,y , mission)