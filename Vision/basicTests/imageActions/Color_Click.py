import cv2
import numpy as np

lower = np.array([110,50,50])
upper = np.array([130,255,255])

cap = cv2.VideoCapture(0)


# Mouse callback function, picks the color of an X and Y point
def pick_color(event,x,y,flags,param):
    global upper #
    global lower # Copied these two lines from Preston's code, ask how it works
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x]
        bgrEdit = np.uint8([[bgr]]) # This line and the chunk below is Preston's code, ask how it works
        color_grab = cv2.cvtColor(bgrEdit,cv2.COLOR_BGR2HSV) #
        lower = np.array([color_grab[0][0][0]-30,color_grab[0][0][1]-30,color_grab[0][0][2]-30]) #
        upper = np.array([color_grab[0][0][0]+30,color_grab[0][0][1]+30,color_grab[0][0][2]+30]) #

while(1):
    
        # Take the frame
        ret, frame = cap.read()
        
        # Displays the normal video stream
        cv2.imshow('image',frame)
        
        #Attach the get_color function so that we can use it.
        cv2.setMouseCallback('image',pick_color)

        # Converts the BGR to HSV
        color_grab = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
         
        # Creates the mask
        mask = cv2.inRange(color_grab, lower, upper)
        
        # Layers the mask onto the frame
        res = cv2.bitwise_and(frame,frame, mask= mask)
        
        # Displays the new frame
        cv2.imshow('mask',res)
        
        if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
            break
cap.release()
cv2.destroyAllWindows()