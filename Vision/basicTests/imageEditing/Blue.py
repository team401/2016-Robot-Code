import cv2
import numpy as np
img = cv2.imread('/home/and3212/Desktop/what.jpg')
img[:,:,1] = 100


cv2.imshow('image',img)
k = cv2.waitKey(5000) & 0xFF
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):
    cv2.imwrite('graycat.png', img)
    cv2.destroyAllWindows()
