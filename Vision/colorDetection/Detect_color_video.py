import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

        # Take the frame
        _, frame = cap.read()

        # Converts the BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

       # Defines the range of colors
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

        lower_green = np.array([30,110,20])
        upper_green = np.array([60,255,255])

        lower_red = np.array([0,30,30])
        upper_red = np.array([0,255,255])
        
        # Threshold the HSV image to get different colors
        b_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        g_mask = cv2.inRange(hsv, lower_green, upper_green)
        r_mask = cv2.inRange(hsv, lower_red, upper_red)
        
        # Bitwise and mask of original frame (3 total)
        b_res = cv2.bitwise_and(frame,frame, mask= b_mask)
        g_res = cv2.bitwise_and(frame,frame, mask= g_mask)
        r_res = cv2.bitwise_and(frame,frame, mask= r_mask)

        cv2.imshow('image',frame)
        cv2.imshow('b_mask',b_mask)
        cv2.imshow('g_mask',g_mask)
        cv2.imshow('r_mask',r_mask)
        cv2.imshow('b_res',b_res)
        cv2.imshow('g_res',g_res)
        cv2.imshow('r_res',r_res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
                break

cv2.destroyAllWindows
