import cv2
import numpy as np

lower = np.array([110,50,50])
upper = np.array([130,255,255])

def get_color(event,x,y,flags,param):
    global lower
    global upper
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = img[y,x]
        formattedBGR = np.uint8([[bgr]])
        hsv_test = cv2.cvtColor(formattedBGR,cv2.COLOR_BGR2HSV)
        lower = np.array([hsv_test[0][0][0]-20,hsv_test[0][0][1]-20,hsv_test[0][0][2]-20])
        upper = np.array([hsv_test[0][0][0]+20,hsv_test[0][0][1]+20,hsv_test[0][0][2]+20])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(img,img, mask= mask)
        cv2.imshow('res',res)

img = cv2.imread("cat.png")
while(1):

    # Displays image
    cv2.imshow('image',img) # opens up a window with image
    
    cv2.setMouseCallback('image',get_color)
    k = cv2.waitKey(0)& 0xFF #Tells it how many milliseconds to stay open, 0 is infinite, a keystroke also kills it
    if k == 27:
       break
cv2.destroyAllWindows()