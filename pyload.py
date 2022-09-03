from threading import Timer
from datetime import datetime
import time,threading,cv2
from folders import *

class Pyload:
    
    def __init__(self , control) :
        self.control = control
    
    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d_%m_%Y %H_%M_%S")

    def calculateDelay(self,time):
        now = datetime.now()
        date_time_obj = datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
        delay = (date_time_obj - now).total_seconds()
        return delay 

    def takeImage(self , src = 0 ):
        cam = cv2.VideoCapture(src)
        _, image = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        return image 

    def saveImage(self,frame,angle , mission):
        createFolder(imageFolder)
        imageName = [self.timeNow() , mission + str(0) + angle].join(",")
        fileName =  imageFolder+ "/" + imageName  +".jpg"
    
        cv2.imwrite( fileName , frame)

    def TakeImageAndSave(self,x,y, mission):
        print("take image")
        self.control.AdcsAngle(x,y)
        img = self.takeImage()
        self.saveImage(img,angle , mission)

    def takeVideoForSeconds(self,duration,x,y , mission) :
        self.control.AdcsAngle(x,y)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        createFolder(videosFolder)
        videoName = [self.timeNow() , mission + str(duration) + angle].join(".")
        fileName =  videosFolder + "/" +  videoName  +".avi"
        out = cv2.VideoWriter(fileName, fourcc, 20.0, (640, 480))
        t = None 
        cap = cv2.VideoCapture(0)
        start = time.time()

        def close():
            print(f'Time: {time.time() - start}')
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        print(duration)
        print(type(duration))
        print(type(int(duration)))
        t = Timer(int(duration), close)
        t.start() 
        ret  =True
        while(ret):
            ret, frame = cap.read()
            out.write(frame)
    
    def takeViderAt(self,time,duration,x,y , mission ):
        delay = self.calculateDelay(time)
        print(delay)
        threading.Timer(delay - 1 , self.takeVideoForSeconds , args=(duration,x,y , mission)).start()
    
    def takeImageAt(self,time,x,y , mission):
        delay = self.calculateDelay(time)
        print(delay)
        threading.Timer(delay - 1, self.TakeImageAndSave ,x,y , mission).start()
    
    def deleteImages(self):
        deleteFolder(imageFolder)

    def deleteVideos(self):
        deleteFolder(videosFolder)
    
    def deleteAll(self):
        self.deleteImages()
        self.deleteVideos()
