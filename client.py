import cv2,socket,pickle,os
import numpy as np
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,500000)
server_ip = "192.168.11.55"
server_port = 6666

cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture(1, cv2.CAP_V4L2)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
width = 1280	
height = 800
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
# cap.set(3, 640)
# cap.set(4, 480)
# cap.set(5,30)
print(cap)
# -1
while True:
	ret,photo = cap.read()
	cv2.imshow('streaming...',photo)
	ret,buffer = cv2.imencode(".jpg",photo,[int(cv2.IMWRITE_JPEG_QUALITY),30])
	x_as_bytes = pickle.dumps(buffer)
	s.sendto((x_as_bytes),(server_ip,server_port))
	print(x_as_bytes)
	if cv2.waitKey(10)==13:
		break
cv2.destroyAllWindows()
cap.release()
