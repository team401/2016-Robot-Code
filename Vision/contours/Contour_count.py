import cv2
import numpy as np

cap = cv2.VideoCapture(0)

#Default lower and upper HSV values. These can replace the get_color function
#If they're set correctly.
lower = np.array([110,50,50])
upper = np.array([130,255,255])

#Kernels for opening and closing. Changing the size of these affects the
#resolution of shapes detected.
kernel = np.ones((10,10),np.uint8)
kernel2 = np.ones((25,25),np.uint8)

#Function to handle mouse events by getting colors. Sets upper and lower to define
#an acceptable HSV range.
def get_color(event,x,y,flags,param):
    global lower
    global upper
    if event == cv2.EVENT_LBUTTONDBLCLK:
        bgr = frame[y,x]
        formattedBGR = np.uint8([[bgr]])
        hsv_test = cv2.cvtColor(formattedBGR,cv2.COLOR_BGR2HSV)
        lower = np.array([hsv_test[0][0][0]-30,hsv_test[0][0][1]-30,hsv_test[0][0][2]-30])
        upper = np.array([hsv_test[0][0][0]+30,hsv_test[0][0][1]+30,hsv_test[0][0][2]+30])

#Run forever displaying video.
while(1):

    #Get the video data.
    ret, frame = cap.read()
    
    # Display raw video.
    cv2.imshow('image', frame)
    
    #Attach the get_color function so that we can use it.
    cv2.setMouseCallback('image',get_color)
    
    #Convert from BGR to HSV so that we can work with it easier.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    #cv2.inRange() takes an HSV image, and two HSV values to look for.
    #inRange was covered earlier, here's a link to where you should have used it:
    #https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html
    #bitwise_and takes an input image, an output image, and mask that specifies
    #which section of the image to apply to. See following link for docs:
    #http://docs.opencv.org/modules/core/doc/operations_on_arrays.html#bitwise-and
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(frame,frame, mask= mask)
    
    #Opening and closing have been covered already.
    #Opening removes noise in the image, closing removes holes in foreground.
    #https://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel2)

    #Threshold the now masked and closed image.
    #OK, I am doing bad things here. This abuses threshold to look at hue values.
    ret,thresh = cv2.threshold(closed,127,255,0)
    
    #Convert the thresholded image to gray so that we can find contours.
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    img, contours, hierarchy = cv2.findContours(gray, 1, 2)
    
    #Try except structure to handle errors before initial upper and lower are
    #changed. Finds contours, places bounding rectangle, and draws a circle at
    #centroid of deteced color section.
    try:
        cnt = contours[0]
        
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        thresh = cv2.circle(thresh,(cx,cy), 3, (0,0,255), -1)
        
        x,y,w,h = cv2.boundingRect(cnt)
        thresh = cv2.rectangle(thresh,(x,y),(x+w,y+h),(0,255,0),2)
    except: 
      pass
  
    #show the final result!
    cv2.imshow('thresh', thresh)
    
    #wait for exit.    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()