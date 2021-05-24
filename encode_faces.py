from imutils import paths
import face_recognition
import pickle
import cv2
import os
import tkinter as tk
import csv
from more_itertools import unique_everseen

root=tk.Tk()
def functionquit():
    root.destroy()
# grab the paths to the input images in our dataset
#print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images("images"))
 
# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []
root.title("Training dataset")
root.configure(background='#232b30')
root.geometry('350x155')

label = tk.Label(root, text="Waiting for task to finish. Do not exit",fg="white",bg="#009999",width=50  ,height=3).grid(row =0)
pl2 = tk.Label(root, text="",fg="white",bg="#009999",width=50  ,height=3).grid(row =1)
quitLabel = tk.Label(root, text="Exit" ,width=20  ,height=3  ,fg="white"  ,bg="#420b0b" ).grid(row=2, columnspan=2)
def task():
# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		l2= tk.Label(root,text=("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths))), fg="white",bg="#009999", height =3, width= 50 ).grid(row=1)
		root.update_idletasks()
		name = imagePath.split(os.path.sep)[-2]
		name_list = name.split(' ')
		idd = name_list[0]
		namee = name_list[1]
		# load the input image and convert it from BGR (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		scale_percent = 80 # percent of original size
		width = int(image.shape[1] * scale_percent / 100) 
		height = int(image.shape[0] * scale_percent / 100) 
		dim = (width, height) 

		# resize image so that dlib doesnt run out of memory
		image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA) 
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
			model="cnn")  #change to cnn for accuracy. takes too much time for dlib without gpu support
	 
		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)
	 
		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)
		row = [idd,namee]
		with open('data2.csv', 'a+', newline='') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)

		csvFile.close()
	# dump the facial encodings + names to disk
	#print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open("encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()
	with open('data2.csv','r') as f1, open('data.csv','w', newline='') as out_file:
		write = csv.writer(out_file)
		write.writerow(['Id','Name'])
		out_file.writelines(unique_everseen(f1))
	os.remove('data2.csv')
	msg=tk.Label(root, text="Task Finished",fg="white",bg="Green",width=50  ,height=3).grid(row=0)
	quitWindow = tk.Button(root, text="Exit", command=functionquit  ,width=20  ,height=3  ,fg="white"  ,bg="#631f1f" ).grid(row=2, columnspan=2)

root.after(100, task)
root.resizable(False,False)
root.mainloop()
