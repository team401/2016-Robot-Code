import cv2
import numpy as np
import urllib.request


# Sets up the webcam and connects to it and initalizes a variable we use for it

stream=urllib.request.urlopen('http://10.4.1.19/mjpg/video.mjpg')
bytes=b''
frame = 0

def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x] # Finds coordinates of the clicked point and picks that color
        bgrEdit = np.uint8([[bgr]]) # This converts the image to HSV and sets the upper
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) # and lower arrays
        print(color_grab)

while(1):
        # Takes frames from the camera that we can use
    bytes+=stream.read(16384)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        img = frame
       
    cv2.imshow('image', frame)
    cv2.setMouseCallback('image', pick_color)
    if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
        break
        
cv2.destroyAllWindows()