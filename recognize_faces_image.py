# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import imutils
import pickle
import cv2
import pandas as pd
import time
import datetime
import os
from PIL import Image
import numpy as np

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "test")

 
for root, dirs,files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root,file)
			pil_image = Image.open(path).convert("L") #converting to grayscale
			image_array = np.array(pil_image, "uint8")
			image = cv2.imread(path)
			scale_percent = 70 # percent of original size
			width = int(image.shape[1] * scale_percent / 100) 
			height = int(image.shape[0] * scale_percent / 100) 
			dim = (width, height) 

			# resize image so that dlib doesnt run out of memory
			image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
			# load the input image and convert it from BGR to RGB
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
			# detect the (x, y)-coordinates of the bounding boxes corresponding
			# to each face in the input image, then compute the facial embeddings
			# for each face
			print("[INFO] recognizing faces...")
			boxes = face_recognition.face_locations(rgb,
				model="cnn") 
			encodings = face_recognition.face_encodings(rgb, boxes)
 
			# initialize the list of names for each face detected
			names = []
			col_names =  ['Id','Name','Date','Time']
			df=pd.read_csv("data.csv", names=col_names)
			attendance = pd.DataFrame(columns = col_names) 
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
 
					# determine the recognized face with the largest number of
					# votes (note: in the event of an unlikely tie Python will
					# select first entry in the dictionary)
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
				# draw the predicted face name on the image
				cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
				y = top - 15 if top - 15 > 15 else top + 15
				cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					0.75, (0, 255, 0), 2)
 
			# show the output image
			cv2.imshow("Image", image)
			key = cv2.waitKey(0) & 0xFF
 
			
			ts = time.time()      
			date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
			timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
			Hour,Minute,Second=timeStamp.split(":")
			fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
			attendance.drop_duplicates(keep=False,inplace=True)
			attendance.to_csv(fileName,index=False)

        	#if the `s` key is pressed, complete exit
			if key == ord("s"):
				break
print('[INFO] exiting')
cv2.destroyAllWindows()