import cv2
import numpy as np

cap = cv2.VideoCapture('/home/and3212/Desktop/Code/FRC/Vision/hungry_cat.MOV')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == 27: # Waitkey is the wait, 27 means you hit esc to kill it 
        break

cap.release()
cv2.destroyAllWindows()
