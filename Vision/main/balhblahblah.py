import cv2
import numpy as np
import urllib.request

check = 1
# Sets up the webcam and connects to it and initalizes a variable we use for it
video =urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
video2 =urllib.request.urlopen('http://192.168.0.91/mjpg/video.mjpg')
bytes=b''
count = 0
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

stream = video

while(True):
    try:
            
        # Takes frames from the camera that we can use
        bytes+=stream.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
           
    #        out.write(frame)
           # Displays the final product
            cv2.imshow('frame',frame)
            count = (count + 1)
            print(count)
            
        if(count >= 100):
            if(check == 1):
                check = 0
                count = 0
                stream = video
    
        if(count >= 100):
            if(check == 0):
                check = 1
                count = 0
                stream = video2
    except:
        pass
     # Hit esc to kill
    if cv2.waitKey(1) ==27:
        exit(0)
            