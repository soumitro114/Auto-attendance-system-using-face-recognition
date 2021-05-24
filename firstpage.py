from tkinter import *
import os
from tkinter import filedialog
import pandas as pd


currdir = os.path.abspath(os.getcwd())
c = currdir+"\Attendance"
root=Tk()

root.configure(background="white")

def function1():
    os.system('python ./encode_faces.py')
def function2():
    os.system('python ./recognize_faces_image.py')
def function3():
    os.system('python ./recognize_faces_video.py')
def function5():    
    os.startfile(os.getcwd()+"/ReadMe.doc");
def function6():
    root.destroy()
def function7():
	root.destroy()
	os.system('python ./newadd.py')
def back():
	root1.destroy()
	os.system('python ./firstpage.py')
def getExcel(): 
        import_file_path = filedialog.askopenfilename(initialdir = c)
        if import_file_path:
	        #df = pd.read_csv (import_file_path)
	        os.startfile(import_file_path)

def total():
	os.system('python ./totalatt.py')

def option():
	root.destroy()
	global root1
	root1=Tk()
	root1.configure(background="white")
	root1.title("AUTO ATTENDANCE SYSTEM")	
	Label(root1, text="AUTO ATTENDANCE SYSTEM",font=("castellar",20),fg="white",bg="#009999",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
	Button(root1,text="Daily attendance",font=("arial",20),bg="#0b4233",fg='white',command=getExcel).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
	Button(root1,text="Total attendance",font=("arial",20),bg="#0b4233",fg='white',command=total).grid(row=4,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
	Button(root1,text="Back",font=('arial',20),bg="#420b0b",fg="white",command=back).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
	root1.mainloop()



root.title("AUTO ATTENDANCE SYSTEM")
Label(root, text="AUTO ATTENDANCE SYSTEM",font=("castellar",20),fg="white",bg="#009999",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Train",font=("arial",20),bg="#0b4233",fg='white',command=function1).grid(row=6,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)
#Button(root,text="Take Attendance(Image)",font=("arial",20),bg="#0b4233",fg='white',command=function2).grid(row=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Take Attendance",font=("arial",20),bg="#0b4233",fg='white',command=function3).grid(row=3,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Show attendance",font=('arial',20),bg="#0b4233",fg="white",command=option).grid(row=5,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Help",font=('arial',20),bg="#0b4233",fg="white",command=function5).grid(row=9,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Add",font=('arial',20),bg="#0b4233",fg="white",command=function7).grid(row=8,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
Button(root,text="Exit",font=('arial',20),bg="#420b0b",fg="white",command=function6).grid(row=10,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

root.resizable(False,False)
root.mainloop()