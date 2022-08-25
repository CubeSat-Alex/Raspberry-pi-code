import os

imageFolder = "images"
videosFolder = "videos"
telemtryFolder = "telemetry"

def createFolder(folderName):
    path = folderName
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

def deleteFolder(path):
    isExist = os.path.exists(path)
    if isExist:
        files_in_dir = os.listdir(path)
        for file in files_in_dir:   
            os.remove(f'{path}/{file}')  
        os.rmdir(path)
