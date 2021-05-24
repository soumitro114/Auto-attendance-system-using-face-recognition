import csv
import os
import glob
import pandas as pd
import time
import datetime
from csv import reader
from os import path
from tkinter import messagebox


currdir = os.path.abspath(os.getcwd())
c = currdir+"\Attendance"
col_names =  ['Id','Name','Date','Time']
if(path.exists("data.csv") == True) :
	pass
	df=pd.read_csv("data.csv", names=col_names)
	lisst = df.Id
	a = {}
	i=1
	while i<len(lisst):
		a[lisst[i]] = 0
		i+=1
	#print(a)
	chck=[]
	base_dir = os.path.dirname(os.path.abspath(__file__))
	image_dir = os.path.join(base_dir, "Attendance")
	count = 0
	for root, dirs,files in os.walk(image_dir):
		for file in files:
			if file.endswith("csv"):
				count+=1
				path = os.path.join(root,file)
				ff = os.path.basename(path)
				os.chdir(c)
				with open(ff, 'rt') as csvfile:
					
					# get number of columns
					for line in csvfile.readlines():
						array = line.split()
						first_item = array[0]
					num_columns = len(array)
					csvfile.seek(0)
					next(csvfile)
					reader = csv.reader(csvfile)
					included_cols = [0]
					for row in reader:
						content = list(row[i] for i in included_cols)
						
						cont = [int(i) for i in content]
	#					print(cont)
						chck = chck + content
	#					print(chck)


	for(k,v) in a.items():
		for i in chck:
			if i==k:
				a[k]+=1

	os.chdir('..')
	with open('ATA_total.csv' , 'w', newline ='') as t, open('data.csv' , 'r') as d :
		writer = csv.writer(t)
		writer2 = csv.reader(d)
		next(writer2)
		writer.writerow(['ID', 'Name', 'Total Present', 'Total class'])
		for (k,v) in a.items():
			for row in writer2:
				writer.writerow([k,row[1],v,count])
				break
	os.startfile(os.getcwd() + './ATA_total.csv')
else:
	messagebox.showerror("Daily attendance files not found", "Make sure there are daily atendance files before trying to generate total attendance")