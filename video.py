import numpy as np
import cv2 as cv
import pytesseract
cap = cv.VideoCapture(1)
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

 # threshold on red color
 lower=(140,30,30)
 upper=(170,60,60)
 mask = cv.inRange(colored, lower, upper)

 # change all non-yellow to white
 filtered = colored.copy()
 filtered[mask!=255] = (255, 255, 255)

 grayed = cv.cvtColor(filtered, cv.COLOR_BGR2GRAY)
 ret,thresh = cv.threshold(grayed,150,255,0)
 contours,hierarchy = cv.findContours(thresh, 1, 2)
 print("Number of contours detected:",len(contours))
 min_y = 999999
 string = None
 arrow_x = None
 arrow_y = None

 for i in range(len(contours)):
    if hierarchy[0][i][3] == -1 and hierarchy[0][i][1] > 10  :
        cv.drawContours(filtered, contours, i, (0,255,255), 3)
    approx = cv.approxPolyDP(contours[i], 0.009 * cv.arcLength(contours[i], True), True) 
    n = approx.ravel()
    i2 = 0
    
    for j in n : 
        if(i2 % 2 == 0): 
            x = n[i2] 
            y = n[i2 + 1] 

            # String containing the co-ordinates. 
            if (min_y > y.item() and y.item() > 10):
                string = str(x) + " " + str(y) 
                min_y = y.item()
                arrow_x = x.item()
                arrow_y = y.item()
        i2 = i2 + 1
#  cv.putText(colored, "Arrow tip", (arrow_x, arrow_y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))
 

  
#  print(arrow_x)
#  print(arrow_y)

 # Mention the installed location of Tesseract-OCR in your system
 # pytesseract.pytesseract.tesseract_cmd = '/usr/local/Cellar/tesseract/5.3.1/bin/tesseract.exe'

 # Read image from which text needs to be extracted

 textImg = colored[(arrow_y - 100) :arrow_y + 10 ,(arrow_x - 150) : (arrow_x + 999)] 
 # Convert the image to gray scale
 grayImg= cv.cvtColor(textImg, cv.COLOR_BGR2GRAY)

 #ret,thresh = cv.threshold(grayImg,255,cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY,11,2)
 thresh = cv.adaptiveThreshold(grayImg,255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 9,7)

 text = pytesseract.image_to_string(thresh,lang='fra') 
 cv.imshow('arrow_location', thresh)
 if len(text) > 0:
    print(text)

 # Display the resulting frame
 cv.imshow('frame', colored)
 if cv.waitKey(1) == ord('q'):
     break          
    # When everything done, release the capture
cap.release()
cv.destroyAllWindows()