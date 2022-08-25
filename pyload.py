from threading import Timer
from datetime import datetime
import time,threading,cv2
from folders import *

class Pyload:
    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d_%m_%Y %H-%M-%S")

    def calculateDelay(self,time):
        now = datetime.now()
        date_time_obj = datetime.strptime(time, '%d/%m/%y %H:%M:%S')
        delay = (date_time_obj - now).total_seconds()
        return delay 

    def takeImage(self):
        cam = cv2.VideoCapture(0)
        _, image = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        return image 

    def saveImage(self,frame):
        createFolder(imageFolder)
        fileName =  imageFolder+ "/" + self.timeNow()  +".jpg"
    
        cv2.imwrite( fileName , frame)

    def TakeImageAndSave(self):
        img = self.takeImage()
        self.saveImage(img)

    def takeVideoForSeconds(self,duration) :
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        createFolder(videosFolder)
        fileName =  videosFolder + "/" + self.timeNow()  +".avi"
        out = cv2.VideoWriter(fileName, fourcc, 30.0, (640, 480))
        t = None 
        cap = cv2.VideoCapture(0)
        start = time.time()

        def close():
            print(f'Time: {time.time() - start}')
            cap.release()
            out.release()
            cv2.destroyAllWindows()
        t = Timer(duration, close)
        t.start() 
        ret  =True
        while(ret):
            ret, frame = cap.read()
            out.write(frame)
    
    def takeViderAt(self,time,duration):
        delay = self.calculateDelay(time)
        print(delay)
        threading.Timer(delay, self.takeVideoForSeconds , args=(duration,)).start()
    
    def takeImageAt(self,time):
        delay = self.calculateDelay(time)
        threading.Timer(delay, self.TakeImageAndSave ).start()
    
    def deleteImages(self):
        deleteFolder(imageFolder)

    def deleteVideos(self):
        deleteFolder(videosFolder)
    
    def deleteAll(self):
        self.deleteImages()
        self.deleteVideos()
