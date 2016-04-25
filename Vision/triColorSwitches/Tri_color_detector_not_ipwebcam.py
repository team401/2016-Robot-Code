import cv2
import numpy as np

focalLength = 222.5
distance = 0

# Creates two different kernels
kernel = np.ones((10,10),np.uint8)
kernel2 = np.ones((25,25),np.uint8)

# This has to be here it doesn't do anything, just look at the trackbar
def nothing():
    pass

# Starts the webcam
cap = cv2.VideoCapture(0)

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
    return radius, thresh
    
def create_ellipse(thresh,cnt):
    ellipse = cv2.fitEllipse(cnt)
    thresh = cv2.ellipse(thresh,ellipse,(0,255,0),2)
    return thresh
    
def create_rectangle(thresh,cnt,cx,cy):
    thresh = cv2.circle(thresh,(cx,cy), 5, (0,0,255), -1)
    x,y,w,h = cv2.boundingRect(cnt)
    thresh = cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),2)

while(1):
 
    # Reads each frame from the video stream
    ret, frame = cap.read()    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Converts the image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
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
    except:
        pass
    # This looks at the trackbar slider, the position changes the color values
    s = cv2.getTrackbarPos(switch,'image')
    try:    
        if s == 0:
            # Range for the Blue Frisbee
            lower = np.array([5,200,200])
            upper = np.array([20,255,255])
            radius, thresh = create_circle(thresh,cnt,cx,cy)
            distance = ((3.5 * focalLength / radius))
#            thresh = create_ellipse(thresh,cnt)
        elif s == 1:
            # Range for the Red Frisbee
            lower = np.array([5,200,200])
            upper = np.array([20,255,255])
            thresh = create_circle(thresh,cnt,cx,cy)
            thresh = create_ellipse(thresh,cnt)
        elif s == 2:
            # Range for the Retroreflective Tape
            lower = np.array([70,195,190])
            upper = np.array([95,255,255])
            thresh = create_rectangle(thresh,cnt,cx,cy)
    except:
        pass
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(thresh,str(round(distance,2)),(500,450), font, 1,(0,0,255),2)
    cv2.putText(thresh,str(round(focalLength,2)),(30,450), font, 1,(0,255,0),2)
        
#    if(distance < 12.00):
#        focalLength = (focalLength + 0.01)
#    if(distance > 12.01):
#        focalLength = (focalLength - 0.01)
    
    # Displays the masked image and the original
    cv2.imshow('image', thresh)
    cv2.imshow('original', frame)
    
    # Lets us use the mouse to find a color        
    cv2.setMouseCallback('original', pick_color)
    
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break
cap.release()    
cv2.destroyAllWindows()