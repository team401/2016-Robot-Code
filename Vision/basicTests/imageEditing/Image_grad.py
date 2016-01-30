import cv2
import numpy as np
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(0)
kernel = np.ones((1,1),np.uint8)

while (True):
    ret, frame = cap.read()
    laplacian = cv2.Laplacian(frame,cv2.CV_64F)
    #closing = cv2.morphologyEx(laplacian, cv2.MORPH_CLOSE, kernel)
    #opening = cv2.morphologyEx(laplacian, cv2.MORPH_OPEN, kernel)
    cv2.imshow('grad',laplacian)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break



# When everything is finished release the capture
cap.release()
cv2.destroyAllWindows()
