import cv2
import numpy as np

# Makes the trackbar work, no idea why
def nothing(x):
    pass

# create a black window image
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('image')

# captures video from webcam or other source
cap = cv2.VideoCapture(0)

# create trackbars for the Edges
cv2.createTrackbar('Min Value','image',0,255,nothing)
cv2.createTrackbar('Max Value','image',0,255,nothing)

while (True):
    # get current position of sliding bars
    Min = cv2.getTrackbarPos('Min Value','image')
    Max = cv2.getTrackbarPos('Max Value','image')

    # gets frame, blurs, it, and then makes it Canny
    ret, frame = cap.read()
    blur = cv2.GaussianBlur(frame,(5,5),0)
    edges = cv2.Canny(blur,Min,Max)
    cv2.imshow('image',edges)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break


# When everything is finished release the capture
cap.release()
cv2.destroyAllWindows()
