import cv2
import numpy as np
from time import sleep

# Sets HSV values for Retro-Reflective Tape
lower = np.array([55,125,180])
upper = np.array([100,255,255])
frame = cv2.imread('../images/distanceTest/test45.png')
check = False
distance = 45 #45 57 81
focalPoint = 1
while(1):
    
    # copy parameters to arrays
    K = np.array(([[1.25790446e+03,0.00000000e+00,6.78148700e+02],[0.00000000e+00,1.25628991e+03,3.90337199e+02],[0.00000000e+00,0.00000000e+00,1.00000000e+00]]))
    d = np.array(([ -4.32680150e-01,-4.78137707e-01,1.52852660e-03,-2.97190159e-03,2.33311192e+00]))

     # just use first two terms (no translation)
    # finds height and width of the original frame
    img = frame
    h, w = img.shape[:2]
    
    # distorts image so it is accurate
    newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0) 
    newimg = cv2.undistort(img, K, d, None, newcamera)
    hsv = cv2.cvtColor(newimg, cv2.COLOR_BGR2HSV)
    # Creates the mask
    mask = cv2.inRange(hsv, lower, upper)
    
    # Layers the mask onto the frame
    res = cv2.bitwise_and(newimg,newimg, mask= mask)
    imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    # Sets max area
    maxArea = -1
    thresholdArea = 500
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > thresholdArea:
            if area > maxArea:
                # Finds max area of masked shapes
                maxArea = area
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                image = cv2.drawContours(res,[box],0,(255,0,0),2)
                
                # Used to find pixel width of the object
                pixelWidth = (rect[1][0])
                
                # Only draws around the the shape with the biggest area
                image = cv2.drawContours(image, cnt, -1, (0,0,255), 3)
                
                # Finds distance
                distance = ((20 * focalPoint) / (pixelWidth))
#                focalPoint = ((pixelWidth * distance) / 20)
                print(distance)
            
                while not check:
                    focalPoint = (focalPoint + 1)
                    sleep(0.01)
                    if distance > (45):
                        check = True
                    break
                
                if distance <= 1:
                    pass
                else:
                    distanceAway = (distance)
                    # Write some Text
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(image,str(round(distanceAway,2)),(500,450), font, 1,(0,0,255),2)
                    cv2.putText(image,str(round(focalPoint,2)),(30,450), font, 1,(0,255,0),2)    
                
    cv2.imshow('image',image)   
    cv2.imshow('original',newimg)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break    
        
cv2.destroyAllWindows()