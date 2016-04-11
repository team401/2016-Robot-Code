import numpy as np
import cv2
import requests
import sys
import linecache
from time import sleep
from networktables import NetworkTable
import logging

logging.basicConfig(level=logging.DEBUG)


NetworkTable.setIPAddress('10.4.1.2')
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
lower = np.array([70,130,220])
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
            crop_frame = frame[800:0, 800:0]
            img = crop_frame

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
        contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        cnt = contours[max_index]

        (x,y),size = cv2.minAreaRect(cnt)
    
        sd.putNumber('xCoord', x)
        sd.putNumber('yCoord', y)     
    
   
    except Exception as e:
        ErrorHandler()
        pass      