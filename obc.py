from ssp import * 
from pyload import *
from orders import *
from client import *
from telemtry  import *
from datetime import datetime
import json

payload = Pyload()
ssp = SSP()
telemtry = Telemtry()
client = Client()

def sendDtring(data):
    jsonData = json.dumps(data)
    print( "Data to sent "+ jsonData)
    packet = ssp.data2Packet(jsonData, Address.GS , Type.Read )
    print("SSP Packet {}".format(packet))
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
        payload.deleteImages()

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
        payload.deleteVideos()

def decodePacket(packet):
    packet = packet.split(',')
    print("Packet Recived : {}".format(packet) )
    recived = ssp.packet2data(packet)
    print(recived)

    recivedJson = json.loads(recived)
    print("Json Data Recived : {}".format(recivedJson) )
    order = recivedJson['order']


    if order == getImageNow :
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
    elif order == getStream :
        print('Start stream at: {}'.format(datetime.now()))
        print("order is to get Stream Now")
        client.stream(0)
    elif order == GEO:
        client.stream("http://192.168.43.1:6677/videofeed?username=CCJDMAFKB&password=") 
    elif order == stopStream : 
        print("order is to stop Stream Now")
        client.stopStream()
    elif order == getTelemetry :
        print("order is to get Telemetry now")
        data = telemtry.get()
        sendDtring(data)
        telemtry.delete()

    elif order == getImages :
        print("order is to get images now")
        sendImages()
    elif order == getVideos :
        print("order is to get videos Now")
        sendVideos()
    elif order == getAllGallery :
        print("order is to get iamges and videos now")
        sendImages()
        sendVideos()
    elif order == getVideoFor :
        duration = recivedJson['args']['duration']
        print('order is to take video for {}'.format(duration)) 
        payload.takeVideoForSeconds(duration)
    elif order == getVideoAt :
        duration = recivedJson['args']['duration']
        time =  recivedJson['args']['time']
        mission =  recivedJson['args']['mission']
        angle =  recivedJson['args']['angle']
        print('order is to take video for {}'.format(duration)) 
        payload.takeViderAt(time , duration,angle , mission)
    elif order == getImageAt :
        time =  recivedJson['args']['time']
        mission =  recivedJson['args']['mission']
        angle =  recivedJson['args']['angle']
        print('order is to take image at {}'.format(time)) 
        payload.takeImageAt(time,angle , mission)