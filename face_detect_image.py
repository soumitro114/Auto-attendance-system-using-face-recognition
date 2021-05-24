#detect faces from image in "test" folder using face_recognition cnn
import face_recognition
import os
import pickle
import cv2
from PIL import Image
import numpy as np
 
base_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(base_dir, "test") 
 
for root, dirs,files in os.walk(image_dir):
	for file in files:
		if file.endswith("png") or file.endswith("jpg"):
			path = os.path.join(root,file)
			pil_image = Image.open(path).convert("L") #converting to grayscale
			image_array = np.array(pil_image, "uint8")
			image = cv2.imread(path)
			# load the input image and convert it from BGR to RGB
			rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 
			# detect the (x, y)-coordinates of the bounding boxes corresponding
			# to each face in the input image, then compute the facial embeddings
			# for each face
			print("[INFO] detecting faces...")
			boxes = face_recognition.face_locations(rgb,
				model="cnn") 
			encodings = face_recognition.face_encodings(rgb, boxes)
						
			names="unknown"
			for (top, right, bottom, left) in boxes:
				# draw the predicted face name on the image
				cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
				y = top - 15 if top - 15 > 15 else top + 15
				#cv2.putText(image, names, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					#0.75, (0, 255, 0), 2)
 
			# show the output image
			cv2.imshow("Image", image)
			key = cv2.waitKey(0) & 0xFF
 
			# if the `s` key is pressed, complete exit
			if key == ord("s"):
				break