from imutils.video import VideoStream
import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import tkinter.ttk as ttk
import tkinter.font as font
import face_recognition
from pathlib import Path
import re
import glob

window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("AUTO ATTENDANCE SYSTEM")

 
window.geometry('730x480')
window.configure(background='#232b30')


#window.grid_rowconfigure(0, weight=1)
#window.grid_columnconfigure(0, weight=1)


message = tk.Label(window, text="Auto attendance System" ,fg="white",bg="#009999",width=32,height=2,font=('times', 30, 'italic bold underline')).grid(row=0)

lbl = tk.Label(window, text="Enter ID :",width=12 ,height=2  ,fg="white"  ,bg="#0b4233" ,font=("arial", 16) )
lbl.place(x=80, y=120)

txt = tk.Entry(window,width=20 , fg="black"  ,bg="#e6e6e6" ,font=("arial", 16))
txt.place(x=270, y=135)

lbl2 = tk.Label(window, text="Enter Name :",width=12  ,height=2  ,fg="white"  ,bg="#0b4233" ,font=("arial", 16)) 
lbl2.place(x=80, y=200)

txt2 = tk.Entry(window,width=20  ,fg="black"  ,bg="#e6e6e6" ,font=("arial", 16) )
txt2.place(x=270, y=210)

lbl3 = tk.Label(window, text="Message : ",width=12  ,height=2  ,fg="white"  ,bg="#0b4233" ,font=("arial", 16)) 
lbl3.place(x=80, y=290)

message = tk.Label(window, text="Enter Name and ID" ,width=20  ,height=3  ,fg="green"  ,bg="#a7bfcf" ,font=("arial", 16)) 
message.place(x=270, y=275)

lbl4 = tk.Label(window, text="Total Pictures :",fg="white"  ,bg="#0b4233" ,font=("arial", 16)) 
lbl4.place(x =545, y= 270)

entry= tk.Entry(window, fg="black" , width=10,bg="#e6e6e6" ,font=("arial", 16) )
entry.place(x=545, y= 315)
entry.insert(0, 20)

def function6():
    window.destroy()
    os.system('python ./firstpage.py')

def functionquit():
    window.destroy()

def clear():
    txt.delete(0, 'end')    
    res = "Cleared"
    message.configure(text= res,bg="#a7bfcf", fg='green')

def clear2():
    txt2.delete(0, 'end')    
    res = "Cleared"
    message.configure(text= res,bg="#a7bfcf", fg='green')    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=(txt.get())
    name=(txt2.get())
    value=int(entry.get())
    if(is_number(Id) and name.isalpha()):
        os.chdir('images')
        dirname = Id+' '+name
        if(os.path.isdir(dirname)):
            files = os.listdir(dirname)
            paths = [os.path.join(dirname, basename) for basename in files]
            latest_file = max(paths, key=os.path.getctime)
            print(latest_file)
            Num=re.split("[_.]", latest_file)[-2]
            sampleNum = int(Num)
        else:
            sampleNum=0

        Path(dirname).mkdir(parents=True, exist_ok=True)
        os.chdir(dirname)
        vs = VideoStream(src=0).start()
        v=sampleNum
        tot=0
        while(True):
            frame = vs.read()
            frame= cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = face_recognition.face_locations(rgb,
            model="cnn")
            for (top,right,bottom,left) in faces:
                res = "Taking Pictures {}/{}".format(tot+1,value)
                message.configure(text= res,bg="#a7bfcf", fg='green')
                window.update_idletasks()
                sampleNum=sampleNum+1
                tot+=1
                #saving the captured face in the dataset folder images
                cv2.imwrite(name +"_ID_"+Id +'_sample_'+ str(sampleNum) + ".jpg",frame[top-60:bottom+40,left-60:right+60])
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)   
                cv2.imshow('Taking photos',frame[top-60:bottom+40,left-60:right+60])
                #incrementing sample number 
                #display the frame
            #cv2.imshow('Taking photos',frame)
            #wait for 200 miliseconds 
            if cv2.waitKey(200) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 21
            elif sampleNum>v+value-1:
                break
        cv2.destroyAllWindows()
        vs.stream.release()
        res = "Images Saved for ID : " + Id +"\nName : "+ name
        message.configure(text= res, fg='white', bg='green')
        os.chdir('..')
        os.chdir('..')
        os.system('python ./encode_faces.py')
        
    else:
        if(is_number(Id)==False):
            res = "Enter Numeric Id"
            message.configure(text= res, bg ='#631f1f', fg= 'white')
        if(name.isalpha()==False):
            res = "Enter Alphabetical Name"
            message.configure(text= res, bg='#631f1f', fg= 'white')

  
clearButton = tk.Button(window, text="Clear", command=clear  ,width=10,fg="white"  ,bg="#0b4233" ,font=("arial", 16))
clearButton.place(x=545, y=123)
clearButton2 = tk.Button(window, text="Clear", command=clear2  ,width=10,fg="white"  ,bg="#0b4233" ,font=("arial", 16))
clearButton2.place(x=545, y=203)    
takeImg = tk.Button(window, text="Add images", command=TakeImages  ,width=12  ,height=2  ,fg="white"  ,bg="green" ,font=("arial", 16))
takeImg.place(x=50, y=380)
quitWindow = tk.Button(window, text="Back", command=function6  ,width=12  ,height=2  ,fg="white"  ,bg="#119af5" ,font=("arial", 16))
quitWindow.place(x=300, y=380)
quitWindow = tk.Button(window, text="Exit", command=functionquit  ,width=12  ,height=2  ,fg="white"  ,bg="#631f1f" ,font=("arial", 16))
quitWindow.place(x=550, y=380)

window.resizable(False,False)
window.mainloop()
