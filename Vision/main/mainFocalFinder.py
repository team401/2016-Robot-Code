import numpy as np
import cv2
import glob

lower = np.array([70,100,225])
upper = np.array([95,255,255])

distance = (178.5) # 8-120.6 10-140.46 12-161.45 14-183.18
#8-117
#10 -136
#12 - 156
#14 - 178.5
focalLength = 0

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,9,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('../images/imagesIPCamera/left9.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
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

        img = cv2.imread('../images/distanceTest/test10.png')
        h,  w = img.shape[:2]
        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        
        # undistort
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        
        
        # crop the image
        x,y,w,h = roi
        dst = dst[y:y+h, x:x+w]

#        cv2.imwrite('calibresult.png',dst)
        
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        # Creates the mask
        mask = cv2.inRange(hsv, lower, upper)
        
        # Layers the mask onto the frame
        res = cv2.bitwise_and(dst,dst, mask= mask)
        imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        try:
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
                        
                        cont = contours[0]
                        M = cv2.moments(cont)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        
#                        image = cv2.drawContours(res,[box],0,(255,0,0),2)
#                        image = cv2.circle(res,(cx,cy), 3, (0,0,255), -1)
                        # Used to find pixel width of the object
                        pixelWidth = (rect[1][0])
                        
                        # Only draws around the the shape with the biggest area
#                        cnt = contours[4]
                        
                        image = cv2.drawContours(res, cont, -5, (0,0,255), 3)

                        
                        # Finds distance
                        focalLength = ((pixelWidth * distance) / 20)
                        print(pixelWidth)
    #                    print('fname is: ' + str(fname))
                        
                        if distance <= 0:
                            pass
                        else:
                            distanceAway = (distance)
                            # Write some Text
                            font = cv2.FONT_HERSHEY_SIMPLEX
                            cv2.putText(image,str(round(distanceAway,2)),(500,450), font, 1,(0,0,255),2)
                            cv2.putText(image,str(round(focalLength,2)),(30,450), font, 1,(0,255,0),2)    
        except:
            pass
        # Draw and display the corners
        cv2.imshow('img',image)

        cv2.waitKey(8000)
        
cv2.destroyAllWindows()