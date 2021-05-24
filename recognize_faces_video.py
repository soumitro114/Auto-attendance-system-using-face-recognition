# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import cv2
import pandas as pd
import time
import datetime

print("[INFO] loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())
 
# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
col_names =  ['Id','Name','Date','Time']
df=pd.read_csv("data.csv", names=col_names)
attendance = pd.DataFrame(columns = col_names) 

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()
	frame= cv2.flip(frame,1)
	
	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

 
	boxes = face_recognition.face_locations(rgb,
		model="cnn")
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

		# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"
 
		# check to see if we have found a match
		if True in matches:
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
 
			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
 
			# determine the recognized face with the largest number
			# of votes (note: in the event of an unlikely tie Python
			# will select first entry in the dictionary)
			name = max(counts, key=counts.get)
			Id = name.split(" ")[0]
			namm = name.split(" ")[1]
			ts = time.time()      
			date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
			attendance.loc[len(attendance)] = [Id,namm,date,timeStamp]   
		# update the list of names
		names.append(name)

	# loop over the recognized faces
	
	for ((top, right, bottom, left), name) in zip(boxes, names):
		
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)
	attendance=attendance.drop_duplicates(subset=['Id'],keep='first')
	cv2.imshow("Video", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		print("[INFO] exiting")
		break
ts = time.time()      
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
Hour,Minute,Second=timeStamp.split(":")
fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
attendance.drop_duplicates(keep=False,inplace=True)
attendance.to_csv(fileName,index=False)

        
cv2.destroyAllWindows()
vs.stop()