import cv2

cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    blur = cv2.GaussianBlur(frame,(5,5),0)
    cv2.imshow('blur',blur)
    if cv2.waitKey(1) & 0xFF == 27: # Hit esc to kill it
        break



# When everything is finished release the capture
cap.release()
cv2.destroyAllWindows()
