from threading import Timer
from datetime import datetime
import time
import os,threading,cv2
from folders import *
from logs import *
from subsytem_control import *

class Pyload:
    
    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d_%m_%Y %H_%M_%S")

    def calculateDelay(self,time):
        now = datetime.now()
        date_time_obj = datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
        delay = (date_time_obj - now).total_seconds()
        return delay 

    def takeImage(self , src = 0 ):
        log.add("Opening camera for image" , LogState.Loading)
        cam = cv2.VideoCapture(src)
        ret, image = cam.read()
        if ret :
            log.add("Image taked succsfully" , LogState.Done)
        else :
            log.add("Can't take image" , LogState.Error)
        cam.release()
        cv2.destroyAllWindows()
        return image 

    def saveImage(self,frame,angle , mission):
        log.add(f"Saving image of misision {mission} to file" , LogState.Loading)
        createFolder(imageFolder)
        imageName = '.'.join([self.timeNow() , mission , str(0) , angle])
        fileName =  imageFolder+ "/" + imageName  +".jpg"
        cv2.imwrite( fileName , frame)
        size = os.path.getsize(fileName)
        print(f"image of misision {mission} saved with {size} bytes")
        log.add(f"image of misision {mission} saved with {size} bytes" , LogState.Done)

    def TakeImageAndSave(self,x,y, mission):
        control.AdcsAngle(x,y)
        time.sleep(15)
        img = self.takeImage()
        self.saveImage(img,f"{x}.{y}" , mission)
        control.AdcsAngle(0,0)

    def takeVideoForSeconds(self,duration,x,y , mission) :
        control.AdcsAngle(x,y)
        time.sleep(15)
        log.add(f"Opening camera for Video for {duration} mission {mission}" , LogState.Loading)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        createFolder(videosFolder)
        videoName = '.'.join([self.timeNow() , mission , str(duration) , f"{x}.{y}"])
        fileName =  videosFolder + "/" +  videoName  +".avi"
        out = cv2.VideoWriter(fileName, fourcc, 20.0, (640, 480))
        t = None 
        cap = cv2.VideoCapture(0)

        def close():
            log.add(f"Recording video stopped" , LogState.Done)
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            size = os.path.getsize(fileName)
            print(f"video of misision {mission} with duration {duration} saved with {size} bytes")
            log.add(f"video of misision {mission} with duration {duration} saved with {size} bytes" , LogState.Done)
            control.AdcsAngle(0,0)
        t = Timer(int(duration), close)
        t.start() 
        ret  =True
        while(ret):
            ret, frame = cap.read()
            out.write(frame)
    
    def takeViderAt(self,time,duration,x,y , mission ):
        delay = self.calculateDelay(time)
        log.add(f"mission {mission} recieved to take video after {delay} for {duration}" , LogState.Done)
        print(delay)
        threading.Timer(delay - 16 , self.takeVideoForSeconds , args=(duration,x,y , mission)).start()
    
    def takeImageAt(self,time,x,y , mission):
        delay = self.calculateDelay(time)
        log.add(f"mission {mission} recieved to take image after {delay}" , LogState.Done)
        print(delay)
        threading.Timer(delay - 16, self.TakeImageAndSave ,args = (x,y , mission)).start()
    
    def deleteImages(self):
        log.add(f"Clearing image storage" , LogState.Loading)
        deleteFolder(imageFolder)
        log.add(f"Images Deleted succesfully" , LogState.Done)

    def deleteVideos(self):
        log.add(f"Clearing video storage" , LogState.Loading)
        deleteFolder(videosFolder)
        log.add(f"Videos Deleted succesfully" , LogState.Done)

payload = Pyload()
