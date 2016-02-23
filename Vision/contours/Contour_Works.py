import cv2
import numpy as np
import requests

lower = np.array([110,50,50])
upper = np.array([130,255,255])

#cap = cv2.VideoCapture(0)
url = 'http://192.168.0.90/mjpg/video.mjpg'
stream = requests.get(url, stream=True)
bytes = b''

# Mouse callback function, picks the color of an X and Y point
def pick_color(event,x,y,flags,param):
    global upper
    global lower
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x] # Finds coordinates of the clicked point and picks that color
        bgrEdit = np.uint8([[bgr]]) # This converts the image to HSV and sets the upper
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) # and lower arrays
        lower = np.array([color_grab[0][0][0]-30,color_grab[0][0][1]-30,color_grab[0][0][2]-30]) #
        upper = np.array([color_grab[0][0][0]+30,color_grab[0][0][1]+30,color_grab[0][0][2]+30]) #

while(1):
    try:
        bytes+=stream.raw.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)

        # Displays the normal video stream
        cv2.imshow('image',frame)
        
        # Attach the get_color function so that we can use it.
        cv2.setMouseCallback('image',pick_color)
    
        # Converts the BGR image to HSV
        color_grab = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
         
        # Creates the mask
        mask = cv2.inRange(color_grab, lower, upper)
        
        # Layers the mask onto the frame
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        # This adds contours to the masked image
        imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        img = cv2.drawContours(res, contours, -1, (0,255,0), 3)
        
        # Displays the new frame
        cv2.imshow('mask',img)
        
        if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
            break
    except Exception as e:
        print e  
cv2.destroyAllWindows()