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


# Sets HSV values for Retro-Reflective Tape
lower = np.array([55,125,180])
upper = np.array([100,255,255])

distance = 0
focalPoint = 918
distanceAway = 0


# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''


def find_marker(frame):
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
    c = max(contours, key = cv2.contourArea)

	# compute the bounding box of the of the paper region and return it
    return cv2.minAreaRect(c), c, image, newimg, res
 
 
def cameraDistance(pixelWidth, focalLength, knownWidth):
	# compute and return the distance from the maker to the camera
	return (pixelWidth * focalLength) / knownWidth

knownDistance = 72
knownWidth = 20

imagePath = ['images/test72.png','images/test239.png']

image = cv2.imread(imagePath[0])
marker = find_marker(image)
focalLength = (marker[1][0] * knownDistance / knownWidth)
print(focalLength)
 
while(1):
    try: 
        # Takes frames from the camera that we can use
        bytes+=stream.read(16384)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR) 
            ret, ret, image, ret = find_marker(frame)
            ret, ret, ret, newimg = find_marker(frame)
            ret, cnt = find_marker(frame)

            M = cv2.moments(cnt)
            try:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00']) 
            except:
                pass
            # Sets max area
            maxArea = -1
            thresholdArea = 500 
            
            marker = find_marker(frame)
            
#            # Only draws around the the shape with the biggest area
            image = cv2.drawContours(image, cnt, -1, (0,0,255), 3)
            
#             Finds distance
            distance = ((20 * marker[1][0]) / focalPoint)
            focalPoint = ((marker[1][0] * distance) / 20)

            ellipse = cv2.fitEllipse(cnt)
            image = cv2.ellipse(image,ellipse,(0,255,0),2)
            (x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
#                        print(angle)
            
            if distance <= 35:
                pass
            else:
                distanceAway = (distance)
                # Write some Text
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image,str(round(distanceAway,2)),(500,450), font, 1,(0,0,255),2)

                cv2.putText(image,str(round(angle,2)),(30,450), font, 1,(0,255,0),2)
                print(focalPoint)
                            
        cv2.imshow('image',frame)   
        cv2.imshow('original',newimg)
#        out.write(image) # Saves all video that it saw through the raw      
        if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
            break                                
    except:
        pass                              

        
cv2.destroyAllWindows()