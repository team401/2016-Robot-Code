import cv2
import numpy as np
import urllib.request
import time
 
 # Sets the current time
now = time.strftime("%c")
current_time = ('%s' %now)

# Names the recorded video with a time stamp
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(current_time + '.avi',fourcc, 20.0, (640,480))

# Creates two different kernels
kernel = np.ones((5,5),np.uint8)
kernel2 = np.ones((10,10),np.uint8)

# This has to be here it doesn't do anything, just look at the trackbar
def nothing():
    pass

# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''

# create a black window image
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# creates a switch for the window
switch = 'B-R-G'
cv2.createTrackbar(switch,'image',0,2,nothing)

# Initializes boundaries for colors
lower = np.array([0,0,0])
upper = np.array([255,255,255])

# This function lets you click on the video, and it returns HSV values of the pixel
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x] # Finds coordinates of the clicked point and picks that color
        bgrEdit = np.uint8([[bgr]]) # This converts the image to HSV and sets the upper
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) # and lower arrays
        print(color_grab)

# The following three functions create an image on the shape
def create_circle(thresh,cnt,cx,cy):
    thresh = cv2.circle(thresh,(cx,cy), 5, (0,0,255), -1)        
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    thresh = cv2.circle(thresh,center,radius,(0,255,0),2)
    return thresh
    
def create_ellipse(thresh,cnt):
    ellipse = cv2.fitEllipse(cnt)
    thresh = cv2.ellipse(thresh,ellipse,(0,255,0),2)
    return thresh
    
def create_rectangle(thresh,cnt,cx,cy):
    thresh = cv2.circle(thresh,(cx,cy), 1, (0,0,0), -1)
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    thresh = cv2.drawContours(thresh,[box],0,(0,0,255),2)
    return thresh

while(1):
    try:
     # Takes frames from the camera that we can use
        bytes+=stream.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) 
            
        # copy parameters to arrays
        K = np.array(([[1.25790446e+03,0.00000000e+00,6.78148700e+02],[0.00000000e+00,1.25628991e+03,3.90337199e+02],[0.00000000e+00,0.00000000e+00,1.00000000e+00]]))
        d = np.array(([ -4.32680150e-01,-4.78137707e-01,1.52852660e-03,-2.97190159e-03,2.33311192e+00]))
        
        # read one of your images
        distort = cv2.imread(frame)
        h, w = distort.shape[:2]
        
        # undistort
        newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0) 
        undistort = cv2.undistort(distort, K, d, None, newcamera)

        
        # Converts the image to HSV
        hsv = cv2.cvtColor(undistort, cv2.COLOR_BGR2HSV)
                
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
            area = cv2.contourArea(cnt)
        except:
            pass
        # This looks at the trackbar slider, the position changes the color values
        s = cv2.getTrackbarPos(switch,'image')
        try:    
            if s == 0:
                # Range for the Blue Frisbee
                lower = np.array([110,200,190])
                upper = np.array([130,255,255])
                thresh = create_circle(thresh,cnt,cx,cy)
                thresh = create_ellipse(thresh,cnt)
            elif s == 1:
                # Range for the Red Frisbee
                lower = np.array([0,145,125])
                upper = np.array([15,200,200])
                thresh = create_circle(thresh,cnt,cx,cy)
                thresh = create_ellipse(thresh,cnt)
            elif s == 2:
                # Range for the Retroreflective Tape
                lower = np.array([60,180,130])
                upper = np.array([100,255,255])
                thresh = create_rectangle(thresh,cnt,cx,cy)
        except:
            pass

        # Displays the masked image and the original
        cv2.imshow('image', thresh)
        cv2.imshow('original', frame)
        cv2.imshow('distort', distort)
        print(area)
        # Lets us use the mouse to find a color        
        cv2.setMouseCallback('original', pick_color)
        out.write(frame) # Saves all video that it saw through the raw
    except:
        pass
    
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
 
        break    
    
cv2.destroyAllWindows()