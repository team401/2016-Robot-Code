import cv2
import numpy as np

lower = np.array([110,50,50])
upper = np.array([130,255,255])

cap = cv2.VideoCapture(0)

kernel = np.ones((10,10),np.uint8)
kernel2 = np.ones((25,25),np.uint8)

# Mouse callback function, picks the color of an X and Y point
def pick_color(event,x,y,flags,param):
    global upper
    global lower
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x] # Finds coordinates of the clicked point and picks that color
        bgrEdit = np.uint8([[bgr]]) # This converts the image to HSV and sets the upper
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) # and lower arrays
        lower = np.array([color_grab[0][0][0]-30,color_grab[0][0][1]-30,color_grab[0][0][2]-30]) 
        upper = np.array([color_grab[0][0][0]+30,color_grab[0][0][1]+30,color_grab[0][0][2]+30]) 

while(1):
    
    # Take the frame and show it
    ret, frame = cap.read()
    cv2.imshow('image',frame)
        
    # Attach the get_color function so that we can use it.
    cv2.setMouseCallback('image',pick_color)

    # Converts the BGR image to HSV
    color_grab = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
         
    # Creates the mask and then layers it onto the frame and then blurs it
    mask = cv2.inRange(color_grab, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)    
    
    ret,thresh = cv2.threshold(opened,127,255,cv2.THRESH_BINARY)
#    blur = cv2.GaussianBlur(res,(5,5),0)
    
    # Converts the image to grayscale because that is easier for contours
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    img, contours, hierarchy = cv2.findContours(gray, 1, 2)

    try:
        # Looks at movements and finds the centroid
        cnt = contours[0]
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
            
        thresh = cv2.circle(thresh,(cx,cy), 5, (0,0,255), -1)
        x,y,w,h = cv2.boundingRect(cnt)
        thresh = cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),2)
    except:
        pass
  
    cv2.imshow('blur', thresh)
        
    if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
        break
        
cap.release()
cv2.destroyAllWindows()