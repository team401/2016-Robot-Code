import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Captures each frame
    ret, frame = cap.read()# Change size by doing
    #ret = cap.set(3,000) & ret = cap.set(4,000)
    ret = cap.set(3,1280)
    ret = cap.set(4,1024)

    # Operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Displays final frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break


# When everything is finished release the capture
cap.release()
cv2.destroyAllWindows()
