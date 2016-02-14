
import cv2
import numpy as np
hull = 0
cnt = 0

img = cv2.imread('../images/distanceTest/failTest.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
thresh = 100

edges = cv2.Canny(blur,thresh,thresh*2)
drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
lol, contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#for cnt in contours[0]:
cnt = contours[0]
hull = cv2.convexHull(cnt)
epsilon = 0.01*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)
(x1, y1) = approx[7][0]
(x2, y2) = approx[6][0]
image = cv2.circle(drawing,(x1,y1), 3, (0,0,255), -1)
image = cv2.circle(drawing,(x2,y2), 3, (0,0,255), -1)
cv2.drawContours(drawing,[approx],0,(0,255,0),1)   # draw contours in green color
cv2.imshow('output',drawing)
cv2.imshow('input',img)

pixelWidthSquared = (pow(x2-x1,2) + pow(y2-y1,2))
pixelWidth = pow(pixelWidthSquared,0.5)

print(pixelWidth)

if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()