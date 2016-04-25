import numpy as np
import cv2
import urllib.request

# Sets up the webcam and connects to it and initalizes a variable we use for it
stream=urllib.request.urlopen('http://192.168.0.90/mjpg/video.mjpg')
bytes=b''

while True:
    try:
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
        
        # read one of your images
        img = frame
        h, w = img.shape[:2]
        
        # undistort
        newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0) 
        newimg = cv2.undistort(img, K, d, None, newcamera)
        
       # Displays the final product
        cv2.imshow('frame', newimg)
    except:
        pass
 # Hit esc to kill
    if cv2.waitKey(1) ==27:
        exit(0)