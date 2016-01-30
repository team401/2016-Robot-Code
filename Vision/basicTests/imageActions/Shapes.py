import numpy as np
import cv2

img = np.zeros((512,512,3,),np.uint8)

img = cv2.line(img,(170,145),(225,195),(100,50,15),10)
img = cv2.rectangle(img,(230,200),(165,140),(30,255,90),3)
img = cv2.circle(img,(305,170), 32, (15,0,255), -1)
img = cv2.circle(img,(305,170), 10, (420,69,420), -1)
img = cv2.ellipse(img,(256,256),(100,50),0,0,180,255,-1)

pts = np.array([[255,212],[285,230],[255,230]], np.int32)
pts = pts.reshape((-1,1,2))
img = cv2.polylines(img,[pts],True,(0,255,255))

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'Leeyum',(10,480), font, 4,(255,255,255),2,cv2.LINE_AA)
cv2.imshow('Face', img)
cv2.waitKey(50000)& 0xFF == ord('q') #Hit 'q' to quit

cap.release()
cv2.destroyAllWindows()
