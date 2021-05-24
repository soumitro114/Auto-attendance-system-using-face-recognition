#detect faces from video stream using face_recognition cnn

from imutils.video import VideoStream
import numpy as np
import imutils
import cv2
import face_recognition

vs = VideoStream(src=0).start()
while True:
	frame = vs.read()
	frame= cv2.flip(frame,1)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	boxes = face_recognition.face_locations(rgb,
		model="cnn") 
	#encodings = face_recognition.face_encodings(rgb, boxes)						
	names="unknown"
	for (top, right, bottom, left) in boxes:
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, names, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)
 		# show the output image
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break