import cv2
import numpy as np

# Mouse callback function
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),100,(255,0,0),-1)

# Create a black image, a window and bind the function to the window
img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('Mouse')
cv2.setMouseCallback('Mouse',draw_circle)

while(1):
    cv2.imshow('Mouse',img)
    if cv2.waitKey(1) & 0xFF == 27:  
        break

cv2.destroyAllWindows()
