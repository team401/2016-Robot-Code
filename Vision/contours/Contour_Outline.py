import cv2

cap = cv2.VideoCapture(0)

while (True):
    

    #Get the video data.
    ret, frame = cap.read()
    
    imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    img = cv2.drawContours(frame, contours, -1, (0,255,0), 3)


    cv2.imshow('image',img)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break