import numpy as np
import cv2
import requests
import sys
import linecache
from time import sleep
from networktables import NetworkTable
import logging



logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) != 2:
    print("Error: specify an IP to connect to!")
    exit(0)

ip = sys.argv[1]

NetworkTable.setIPAddress(ip)
NetworkTable.setClientMode()
NetworkTable.initialize()

sd = NetworkTable.getTable("SmartDashboard")



def ErrorHandler():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    line = linecache.getline(filename, lineno, f.f_globals)
    print 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    

# Sets the HSV range for the Retro-Reflective Tape
lower = np.array([70,215,220])
upper = np.array([100,255,255])

# Initializes distance, focalLength, and the count
focalLength = 730.5

#Wait for IP camera to connect. Will not exit until this works
while(True):
    try:
        url = 'http://10.4.1.19/mjpg/video.mjpg'
        stream = requests.get(url, stream=True)
        bytes = b''
        print('Connected to IP Camera')
        break
    except:
        sleep(0.5)
        print('No cam yet')
        pass

#Import the undistortion matrix and set up dist
mtx = np.genfromtxt('/home/ubuntu/Desktop/Code/2016-Robot-Code/Vision/main/mtx.txt')
dist = np.array([ -5.08941357e-01,-2.73762518e-02,2.94200341e-03,1.50764126e-03,2.12977986e+00])

    
while(True):

    distance = 0
    angle = 0 
    
    
    # When nothing is seen there is a divide by zero error, so this skips over that
    try:
        # Takes frames from the camera that we can use
        bytes+=stream.raw.read(16384)
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
        #dst = dst[0:400, 0:640]
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        
        # Creates the mask for the Retro-Reflective tape
        mask = cv2.inRange(hsv, lower, upper)
        
        # Layers the mask onto the frame
        res = cv2.bitwise_and(dst,dst, mask= mask)
        imgray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        ret,thresh = cv2.threshold(imgray,127,255,0)
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        
        # Sets max area
        maxArea = 0
        thresholdArea = 500
        
        if(len(contours) == 0):
            distance = 0
        else:
		
	    areas = [cv2.contourArea(c) for c in contours]
	    max_index = np.argmax(areas)
	    cnt = contours[max_index]
 
            rect = cv2.minAreaRect(cnt)
            box = cv2.cv.BoxPoints(rect)
            box = np.int0(box)
            
            # Finds countours and center of the goal
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            ellipse = cv2.fitEllipse(cnt)
            image = cv2.ellipse(res,ellipse,(0,255,0),0)
            (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
    
    
            epsilon = 0.01*cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,epsilon,True)
  	    #print len(approx)
            if angle >= 90:
                (x1, y1) = approx[1][0] # Approx 1,2 is bottom width
                (x2, y2) = approx[2][0]
                (sx1,sy1) = approx[0][0] # Approx 0,1 is side width 1
                (sx2,sy2) = approx[3][0] # Approx 2,3 is side width 2
            elif angle < 90:
                (x1, y1) = approx[6][0] # Approx 6,7 is bottom width
                (x2, y2) = approx[7][0]
                (sx1,sy1) = approx[5][0] # Approx 5,6 is side width 1
                (sx2,sy2) = approx[0][0] # Approx 7, 0 is side width 2                            
    
            #cv2.drawContours(image,[approx],0,(0,0,255),1)
            
            bottomWidthSquared = (pow(x2-x1,2) + pow(y2-y1,2))
            side1Squared = (pow(sx1-x1,2) + pow(sy1-y1,2))
            side2Squared = (pow(sx2-x2,2) + pow(sy2-y2,2))
            
            bottomWidth = pow(bottomWidthSquared,0.5)
            side1 = pow(side1Squared,0.5)
            side2 = pow(side2Squared,0.5)
            
                    
                    
            if(side1 >= side2):
                
                if(side1/side2 >= 1.25):
                    distance = ((12 * focalLength) / side1)
                    
                else:
                    distance = ((20 * focalLength / bottomWidth))
                    
            else:
                
                if(side2/side1 >= 1.25):
                    distance = ((12 * focalLength) / side2)
                   
                else:
                    distance = ((20 * focalLength / bottomWidth))


        if(distance > 300 or distance < 30):
            pass
   
        try:
            print('robotTime:', sd.getNumber('robotTime'))
        except KeyError:
            print('robotTime: N/A')

        sd.putNumber('distance', distance)
        sd.putNumber('angle', angle)
        sd.putNumber('x', x)
        sd.putNumber('y', y)     
    
   
    except Exception as e:
        ErrorHandler()
        pass      
    
    if cv2.waitKey(1) & 0xFF == 27: # esc is the kill key
            break

cv2.destroyAllWindows()
