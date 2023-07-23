import numpy as np
import cv2 as cv
import pytesseract
cap = cv.VideoCapture(1)
width = 1280	
height = 800
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

if not cap.isOpened():
 print("Cannot open camera")
 exit()
while True:
 # Capture frame-by-frame
 ret, frame = cap.read()
 # if frame is read correctly ret is True
 if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    break
 # Our operations on the frame come here
 #  gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
 colored = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

 # Display the resulting frame
 cv.imshow('frame', colored)
 if cv.waitKey(1) == ord('q'):
     break          
    # When everything done, release the capture
cap.release()
cv.destroyAllWindows()