import cv2
import numpy as np
import urllib.request
import threading
from time import sleep

lock=threading.Lock()

# Sets up the webcam and connects to it and initalizes a variable we use for it
videoLeft = urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytesLeft = b''
capLeft = 'left'

videoRight = urllib.request.urlopen('http://192.168.0.91/mjpg/video.mjpg')
bytesRight = b''
capRight = 'right'

def capture(stream, bytes, name):
    while(True):
        lock.acquire()
        try:
            cv2.waitKey(1)
            # Takes frames from the camera that we can use

            bytes+=stream.read(16384)

            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')

            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

               # Displays the final product
                cv2.imshow(name, frame)
                
        except:
            pass
        lock.release()

    
a = threading.Thread(target=capture, args = [videoLeft, bytesLeft, capLeft])
b = threading.Thread(target=capture, args = [videoRight, bytesRight, capRight])

a.start()
b.start()


a.join()
b.join()