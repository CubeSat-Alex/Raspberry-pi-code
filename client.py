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
          
    def sendFrame(self,frame):
#         frame = cv2.resize(frame,(0,0),fx = 0.4, fy = 0.4)
        frame = imutils.resize(frame,width=320)
        a = pickle.dumps(frame)
        message = struct.pack("Q",len(a))+a
        self.clientSocket.sendall(message)
    
    def stream(self,where):
        while True:
            if self.clientSocket:
                self.vid = cv2.VideoCapture(where)
                while(self.vid.isOpened()):
                    ret , frame = self.vid.read()
                    if ret == True:
                        start = datetime.now()
                        self.sendFrame(frame)
                        print('Time after sending frame: {}'.format(datetime.now()- start))

                else: 
                    break
    
    def stopStream(self):
        self.vid.release()
        cv2.destroyAllWindows()

    def sendVideo(self,videoName):
        cap = cv2.VideoCapture(videoName)
        print("sending")

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
        print("sending")
        self.sendFrame(img)

    def dispose(self):
        self.serverSocket.close()