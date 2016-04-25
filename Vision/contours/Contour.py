import numpy as np
import cv2
cap = cv2.VideoCapture(0)

while (True):
    
    ret, frame = cap.read()
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(imgray, contours, -1, (0,255,0), 3) # all contours
    img = cv2.drawContours(imgray, contours, 3, (0,255,0), 3)
    cnt = contours[4]
    img = cv2.drawContours(imgray, [cnt], 0, (0,255,0), 3)

    M = cv2.moments(cnt)
    print(M)

    cv2.imshow('frame', imgray)
    if cv2.waitKey(1) & 0xFF == 27: # Waitkey is the wait, 27 means you hit esc to kill it 
        break

cap.release()
cv2.destroyAllWindows()
