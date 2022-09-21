import time as time
import threading , json
from xmlrpc.client import DateTime
from ssp import * 
from pyload import *
from orders import *
from client import *
from telemtry  import *
from logs import *
from datetime import datetime
from subsytem_control import *
from leds import *
import os
from storage import *

streamIp = "192.168.43.1"
streamName = "CCJDMAAAFKB"


def sendDtring(data):
    timeNow = datetime.now()
    leds.ledOn(Leds.Download)
    jsonData = json.dumps(data)
    print( "Data to sent "+ jsonData)
    packet = ssp.data2Packet(jsonData, Address.GS , Type.Read )
#     print("recieved SSP Packet {}".format(packet))
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
            print("data send succesfully")
            client.senData("end of data")
            print(datetime.now() - timeNow)
            leds.ledOf(Leds.Download)
            break 

def sendImages():
    leds.ledOn(Leds.Download)
    path = imageFolder
    isExist = os.path.exists(path)
    if isExist:
        files_in_dir = os.listdir(path)
        imageLenght = len(files_in_dir)
        data = {"imageLenght" : imageLenght  , "imagesNames" : files_in_dir}
        sendDtring(data)
        print(f"number of images is {imageLenght} ")
        leds.ledOn(Leds.Download)
        time.sleep(0.1)
        for file in files_in_dir:
            now = datetime.now()
            client.sendImage(f'{path}/{file}')
            print(f"image take {datetime.now() - now}")
            time.sleep(0.5)
    
    leds.ledOf(Leds.Download)

def sendVideos():
    leds.ledOn(Leds.Download)
    path = videosFolder
    isExist = os.path.exists(path)
    if isExist:
        files_in_dir = os.listdir(path)
        videosLenght = len(files_in_dir)
        data = {"videosLenght" : videosLenght  , "VideosNames" : files_in_dir}
        sendDtring(data)
        print(f"number of videos is {videosLenght} ")
        leds.ledOn(Leds.Download)
        time.sleep(1)
        for file in files_in_dir:
            now = datetime.now()
            client.sendVideo(f'{path}/{file}')
            print(f"video take {datetime.now() - now}")
            time.sleep(2)
    leds.ledOf(Leds.Download)

def decodePacket(packet):
    try :
        packet = packet.split(',')
        recived = ssp.packet2data(packet)
    except :
        return 

    recivedJson = json.loads(recived)
    command = recivedJson['order']
    if command != ping :
        print("revived SSPV2 Packet  : {}".format(packet))
        print("decodded Data Recived : {}".format(recivedJson) )
        log.add("An order recieved with data {}".format(recivedJson) , LogState.Done)

    if command == ping :
        pass
#         print("Server checked me")
#         log.add("Server ping recieved", LogState.Done)
    elif command == getImageNow :
        print("Order is to get image now and send it")
        frame = payload.takeImage()
        try :
            print("Image taked succesfully , sending")
            start = datetime.now() 
            client.sendFrame(frame,True)
            print('Time after sending picture: {}'.format(datetime.now() - start))
        except :
            print("An error happened while takeing the photo")
    elif command == getStream :
        leds.ledOn(Leds.Stream)
        log.add("Start Stream request", LogState.Loading)
        print('Start stream at: {}'.format(datetime.now()))
        print("order is to get Stream Now")
#         try :
#         streamUrl = "http://"+streamIp+":6677/videofeed?username="+streamName+"&password="
        client.stream(0)
#         except :
#             print("error at streaming")
#             leds.ledOf(Leds.Stream)
#             log.add("An error hapeened while streaming" , LogState.Error)
    elif command == stopStream : 
        leds.ledOf(Leds.Stream)
        print("order is to stop Stream Now")
        log.add("Stop streaming" , LogState.Done)
        client.stopStream()
    elif command == getTime :
        print("order is get time now")
        now = datetime.now()
        data = now.strftime("%d-%m-%Y %H:%M:%S")
        log.add(f"Send time to ground station {data}" , LogState.Done)
        print("Time now in RPI is ",data)
        sendDtring(data)
    elif command == setTime :
        print("order is set time now")
        wanted_time = recivedJson['args']['requestTime'] 
        log.add(f"set OBC time from {datetime.now()} to {wanted_time}" , LogState.Done)
        dateTime = datetime.strptime(wanted_time, '%d-%m-%Y %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        print("Requested time is " , dateTime)
#         os.system("sudo systemctl stop systemd-timesyncd")
#         os.system("sudo systemctl disable systemd-timesyncd")
        print(os.system("sudo date -s '{}'".format(dateTime)))
        print(f" time after set is {datetime.now()}")
    elif command ==  setNextSession :
        print("order is set next session")
        start = recivedJson['args']['start'] 
        startTime = datetime.strptime(start, '%d-%m-%Y %H:%M:%S')
        end = recivedJson['args']['end'] 
        endTime = datetime.strptime(end, '%d-%m-%Y %H:%M:%S')
        now = datetime.now()
        toStart = (startTime - now).total_seconds()
        duration = (endTime - startTime).total_seconds()
        log.add(f"set next session time at {startTime} and end at {endTime}" , LogState.Done)

        def nextSession(duration):
            log.add(f"Session opened and will close after {duration}" , LogState.Done)
            print("next session is now and end after",duration)
            leds.ledOn(Leds.Session)
            def closeSession():
                leds.ledOf(Leds.Session)
                log.add("Session closes" , LogState.Done)
                print("session closed ") 
            threading.Timer(duration, closeSession).start()

        threading.Timer(toStart, nextSession ,args = (duration,)).start()
    elif command == subsytemControl :
        log.add("Order is subsytem control" , LogState.Done)
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
            print(f"X {args['X']} , Y {args['Y']} ")
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
        log.add("Sending telemtry to ground station " , LogState.Done)
        print("order is to get Telemetry now")
        data = telemtry.get()
        sendDtring(data)
    elif command == deleteTelemetry :
        print("order is to delete telemetry")
        telemtry.delete()
    elif command == getLogs :
        log.add("Sending Logs to ground station " , LogState.Done)
        print("order is to get Logs now")
        data = log.get()
        sendDtring(data)
    elif command == deleteLogs :
        print("order is to delete logs")
        log.delete()
    elif command == getImages :
        log.add("Sending images to ground station " , LogState.Done)
        print("order is to get images now")
        sendImages()
    elif command == getVideos :
        log.add("Sending Videos to ground station " , LogState.Done)
        print("order is to get videos Now")
        sendVideos()
        print("sending finished")
    elif command == deleteImages :
        print("order is to delete images Now")
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
    elif command == getStorages :
        sendDtring(storage.getStorage())