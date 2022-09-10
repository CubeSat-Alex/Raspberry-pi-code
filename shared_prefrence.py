import json

class Cache:
    def add(self , key , value):
        f = open( "cache.txt" ,'r+')
        data = f.read()
        if len(data) == 1 :
            data = {}
        else :
            data = json.loads(data)
        data[key] = value
        f.seek(0)
        f.truncate() 
        data = json.dumps(data)
        f.write(data)
        f.close()
        
    def get(self , key):
        f = open( "cache.txt" ,'r')
        data = f.read()
        if len(data) == 1 :
            data = {}
        else :
            data = json.loads(data)
        try :
            value = data[key]
        except :
            value = 0 
        f.close()
        return value 