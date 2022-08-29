from threading import Timer
from datetime import datetime
import time,threading,cv2
from folders import *

class Pyload:
    def timeNow(self) :
        now = datetime.now()
        return now.strftime("%d_%m_%Y %H_%M_%S")

    def calculateDelay(self,time):
        now = datetime.now()
        date_time_obj = datetime.strptime(time, '%d/%m/%Y %H:%M:%S')
        delay = (date_time_obj - now).total_seconds()
        return delay 

    def takeImage(self):
        cam = cv2.VideoCapture(0)
        _, image = cam.read()
        cam.release()
        cv2.destroyAllWindows()
        return image 

    def saveImage(self,frame,angle , mission):
        createFolder(imageFolder)
        imageName = [self.timeNow() , mission + str(0) + angle].join(",")
        fileName =  imageFolder+ "/" + imageName  +".jpg"
    
        cv2.imwrite( fileName , frame)

    def TakeImageAndSave(self,angle , mission):
        print("take image")
        img = self.takeImage()
        self.saveImage(img,angle , mission)

    def takeVideoForSeconds(self,duration,angle , mission) :
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
    
    def takeViderAt(self,time,duration,angle , mission ):
        delay = self.calculateDelay(time)
        print(delay)
        threading.Timer(delay, self.takeVideoForSeconds , args=(duration,angle , mission)).start()
    
    def takeImageAt(self,time,angle , mission):
        delay = self.calculateDelay(time)
        print(delay)
        threading.Timer(delay, self.TakeImageAndSave ,angle , mission).start()
    
    def deleteImages(self):
        deleteFolder(imageFolder)

    def deleteVideos(self):
        deleteFolder(videosFolder)
    
    def deleteAll(self):
        self.deleteImages()
        self.deleteVideos()
