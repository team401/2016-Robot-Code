import cv2
import numpy as np
import urllib.request

# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''

# Creates two different kernels
kernel = np.ones((10,10),np.uint8)
kernel2 = np.ones((25,25),np.uint8)

# This has to be here it doesn't do anything, just look at the trackbar
def nothing():
    pass

# create a black window image
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# creates a switch for the window
switch = 'BRG'
cv2.createTrackbar(switch,'image',0,2,nothing)


while(1):
    # We need a try statement because the camera doesn't load immediately and this crashes the program
    try:
        # This gets the data from the IP Webcam and lets us take data from it
        bytes+=stream.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
         
        # Converts the image to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        # This looks at the trackbar slider, the position changes the color values
        s = cv2.getTrackbarPos(switch,'image')
        if s == 0:
            # Range for the Blue Frisbee
            lower = np.array([110,140,150])
            upper = np.array([130,200,255])
        elif s == 1:
            # Range for the Red Frisbee
            lower = np.array([0,145,125])
            upper = np.array([15,200,200])
        elif s == 2:
            # Range for the Retroreflective Tape
            lower = np.array([85,205,245])
            upper = np.array([95,225,255])
            
        # Creates a mask using the upper and lower we got from above and applies it to the video stream
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        # Starts opening and closing kernels to remove noise and holes
        opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)    
        
        # Creates a threshold that we overwrite later
        ret,thresh = cv2.threshold(closed,127,255,cv2.THRESH_BINARY)
        
        # Turns the video stream into a gray version so we can find contours and stuff
        gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
        img, contours, hierarchy = cv2.findContours(gray, 1, 2)
        
        # This structure is here because the first time the code run it divides by 0
        try:
            # Looks at movements and finds the center of large shapes
            cnt = contours[0]
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])       
            
            # Puts an ellipse around the object
            ellipse = cv2.fitEllipse(cnt)
            thresh = cv2.ellipse(thresh,ellipse,(0,255,0),2)
    
            # Puts a circle around the object
            thresh = cv2.circle(thresh,(cx,cy), 5, (0,0,255), -1)        
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            thresh = cv2.circle(thresh,center,radius,(0,255,0),2)
        except:
            pass
    
        # Displays the masked image and the original
        cv2.imshow('image', thresh)
        cv2.imshow('original', frame)
        
        if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
            break
    except:
        pass
cv2.destroyAllWindows()