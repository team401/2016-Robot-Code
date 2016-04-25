import cv2
import numpy as np

img = cv2.imread("cat.png")
img[:,:,2] = 0
img[:,:,1] = 0
print(img[:,:,2])
while(1):

    cv2.imshow('image',img) # opens up a window with image

    k = cv2.waitKey(0)& 0xFF #Tells it how many milliseconds to stay open, 0 is infinite, a keystroke also kills it
    if k == 27:
       break
cv2.destroyAllWindows()