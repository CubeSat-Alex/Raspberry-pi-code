import socket,cv2, pickle,struct,imutils
from datetime import datetime


class Client:
    ip = "192.168.43.103"
    port = 5005 

    def __init__(self):
        self.clientSocket = socket.socket()
    
    def connect(self):
        self.clientSocket.connect((self.ip,self.port))
    
    def recieveData(self):
        try :
            dataFromClient = self.clientSocket.recv(1024*4)
            return dataFromClient.decode()
        except :
            return 0
    
    def senData(self , data):
        try :
            self.clientSocket.send(data.encode())
            return 1
        except:
            return 0
    
    frames = 0 
    def sendFrame(self,frame):
        self.frames = self.frames +  1
#         print(self.frames)
        frame = imutils.resize(frame,width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        self.clientSocket.sendall(message)
    
    def stream(self,where):
        print(f"start at {datetime.now()}");
        while True:
            if self.clientSocket:
                self.vid = cv2.VideoCapture(where)
                frameNumber = 0 
                while(self.vid.isOpened()):
                    ret , frame = self.vid.read()
                    if ret == True:
                        frameNumber = frameNumber + 1
                        print('Time when sending frame {} is {}'.format(frameNumber ,datetime.now()))
                        self.sendFrame(frame)
                else: 
                    break
    
    def stopStream(self):
        print(f"stop at {datetime.now()}");
        print(f"number of frames {self.frames}");
        self.vid.release()
        cv2.destroyAllWindows()

    def sendVideo(self,videoName):
        self.frames = 0
        cap = cv2.VideoCapture(videoName)
        print("sending...")

        if (cap.isOpened()== False): 
            return 
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                self.sendFrame(frame)
            else: 
                break

        cap.release()
        cv2.destroyAllWindows()

    def sendImage(self,imageName):
        img = cv2.imread(imageName , cv2.IMREAD_COLOR)
        self.sendFrame(img)

    def dispose(self):
        self.clientSocket.close()
        self.clientSocket = socket.socket()

client = Client()
