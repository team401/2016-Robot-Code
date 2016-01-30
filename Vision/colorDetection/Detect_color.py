import cv2
import numpy as np

img = cv2.imread('/home/and3212/Desktop/Code/FRC/Vision/cat.png')

while(1):

        # Converts the BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Defines the range of colors
        lower_blue = np.array([0,50,50])
        upper_blue = np.array([255,255,255])

        lower_red = np.array([50,50,0])
        upper_red = np.array([255,255,255])

        lower_green = np.array([50,0,50])
        upper_green = np.array([255,255,255])

        # Threshold the HSV image to get different colors
        b_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        g_mask = cv2.inRange(hsv, lower_green, upper_green)
        r_mask = cv2.inRange(hsv, lower_red, upper_red)

        # Bitwise and mask of original frame (3 total)
        b_res = cv2.bitwise_and(img,img, b_mask= b_mask)
        g_res = cv2.bitwise_and(img,img, g_mask= g_mask)
        r_res = cv2.bitwise_and(img,img, r_mask= r_mask)

        cv2.imshow('image',img)
        cv2.imshow('b_mask',b_mask)
        cv2.imshow('g_mask',g_mask)
        cv2.imshow('r_mask',r_mask)
        cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
                break

cv2.destroyAllWindows
