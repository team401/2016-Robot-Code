import cv2
import numpy as np

cap = cv2.VideoCapture(0)

lower = np.array([110,50,50])
upper = np.array([130,255,255])
kernel = np.ones((10,10),np.uint8)
kernel2 = np.ones((25,25),np.uint8)

def get_color(event,x,y,flags,param):
    global lower
    global upper
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x]
        formattedBGR = np.uint8([[bgr]])
        hsv_test = cv2.cvtColor(formattedBGR,cv2.COLOR_BGR2HSV)
        lower = np.array([hsv_test[0][0][0]-30,hsv_test[0][0][1]-30,hsv_test[0][0][2]-30])
        upper = np.array([hsv_test[0][0][0]+30,hsv_test[0][0][1]+30,hsv_test[0][0][2]+30])

while(1):

    ret, frame = cap.read()
    # Displays image
    cv2.imshow('image', frame) # opens up a window with image
    
    cv2.setMouseCallback('image',get_color)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)
    
    ret,thresh = cv2.threshold(closed,127,255,0)
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    img, contours, hierarchy = cv2.findContours(gray, 1, 2)
    try:
        cnt = contours[0]
        
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        thresh = cv2.circle(thresh,(cx,cy), 3, (0,0,255), -1)
        
        x,y,w,h = cv2.boundingRect(cnt)
        thresh = cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),2)
    except: 
      pass
    cv2.imshow('thresh', thresh)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()