import cv2
import numpy as np
import urllib.request
import time


 # Sets the current time
now = time.strftime("%c")
current_time = ('%s' %now)

# Names the recorded video with a time stamp
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(current_time + '.avi',fourcc, 20.0, (640,480))

# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''

# Sets HSV values for Retro-Reflective Tape
lower = np.array([55,125,180])
upper = np.array([100,255,255])

distance = 239
focalPoint = 525.8
distanceAway = 0
while(1):

 # Takes frames from the camera that we can use
    bytes+=stream.read(16384)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) 
        
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
                    pixelWidth = (rect[1][1])
#                    print(pixelWidth)
                    
                    # Only draws around the the shape with the biggest area
                    image = cv2.drawContours(image, cnt, -1, (0,0,255), 3)
                    
                    # Finds distance
#                    distance = ((20 * pixelWidth) / focalPoint)
                    focalPoint = ((pixelWidth * distance) / 20)

                    if distance <= 50:
                        pass
                    else:
                        distanceAway = (distance)
                    
                        print(focalPoint)
                                        
        cv2.imshow('image',image)   
        if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
         
            break    
        
cv2.destroyAllWindows()

#230.5inches