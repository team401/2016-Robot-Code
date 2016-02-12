import numpy as np
import cv2
import urllib.request

# Sets the HSV range for the Retro-Reflective Tape
lower = np.array([70,100,225])
upper = np.array([95,255,255])

# Initializes distance, focalLength, and the count
distance = 0 
focalLength = 730.5
count = 10

# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,9,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

# Calibrates it using the 9th chess image and makes it gray
img = cv2.imread('../images/imagesIPCamera/left9.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the chess board corners, it's a 9x6 board
ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)
    corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    imgpoints.append(corners2)
    img = cv2.drawChessboardCorners(img, (9,6), corners2,ret)
    
    #ret is float, mtx is 3x3 array of float64, rvces is list of arrays of float64, tvecs is list of array of float64
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    dist = np.array([ -5.08941357e-01,-2.73762518e-02,2.94200341e-03,1.50764126e-03,2.12977986e+00])

    
while(True):
    # When nothing is seen there is a divide by zero error, so this skips over that
    try:
        # For every ~10th frame
        if count >= (10):
            # Takes frames from the camera that we can use
            bytes+=stream.read(16384)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                img = frame

            h,  w = img.shape[:2]
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            
            # undistorts
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
             
            # crop the image and converts it to HSV
            x,y,w,h = roi
            dst = dst[y:y+h, x:x+w]
            hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
            
            # Creates the mask for the Retro-Reflective tape
            mask = cv2.inRange(hsv, lower, upper)
            
            # Layers the mask onto the frame
            res = cv2.bitwise_and(dst,dst, mask= mask)
            imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
            ret,thresh = cv2.threshold(imgray,127,255,0)
            image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            count = 1
            
            
            # Sets max area
            maxArea = 0
            thresholdArea = 500
            for cnt in contours:
                area = cv2.contourArea(cnt)
                
                # Only find the biggest goal that is seen
                if area > thresholdArea:
                    if area > maxArea:
                        # Finds max area of masked shapes
                        maxArea = area
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        
                        # Finds countours and center of the goal
                        cont = contours[0]
                        M = cv2.moments(cont)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        
                        # Draws the countours and a circle around the goal
                        image = cv2.drawContours(res,[box],0,(255,0,0),2)
                        image = cv2.circle(res,(cx,cy), 3, (0,0,255), -1)
                        
                        # Used to find pixel width of the object
                        pixelWidth = (rect[1][0])
                        
                        # Only draws around the the shape with the biggest area
#                        image = cv2.drawContours(image, cnt, -1, (0,0,255), 3)
                        
                        # Finds distance
                        distance = ((20 * focalLength) / (pixelWidth))
                        # Removes noise by filtering out things with a volume of less than 20
                        print(pixelWidth)
                        if distance <= 10:
                            pass
                        else:
                            # displays the Angle, Distance, and Focal Length
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.putText(image,str(round(distance,2)),(500,450), font, 1,(0,0,255),2)
#                            cv2.putText(image,str(round(angle,2)),(500,650), font, 1,(255,0,0),2)
                            cv2.putText(image,str(round(focalLength,2)),(30,450), font, 1,(0,255,0),2)
                
        # Shows the image and adds one to the count
        count = count + 1
        cv2.imshow('img',image) 

    except:
        pass        

    if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
            break

cv2.destroyAllWindows()