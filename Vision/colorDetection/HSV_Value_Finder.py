import cv2
import numpy as np
import requests
from time import sleep

#Wait for IP camera to connect. Will not exit until this works
while(True):
    try:
        url = 'http://10.4.1.19/mjpg/video.mjpg'
        stream = requests.get(url, stream=True)
        bytes = b''
        print('Connected to IP Camera')
        break
    except:
        sleep(0.5)
        print('No cam yet')
        pass


def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x] # Finds coordinates of the clicked point and picks that color
        bgrEdit = np.uint8([[bgr]]) # This converts the image to HSV and sets the upper
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) # and lower arrays
        print(color_grab)

while(1):
    try:
        # Takes frames from the camera that we can use
        bytes+=stream.raw.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            crop_frame = frame[0:380, 0:640]
            img = crop_frame
       
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', pick_color)
        if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
            break
    except:
        pass
cv2.destroyAllWindows()