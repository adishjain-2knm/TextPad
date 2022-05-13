import tkinter
from tkinter import BOTH, END, INSERT, RIGHT, VERTICAL, Y, Button, Frame, Scrollbar, Text, Tk, messagebox
#from tkinter import ttk
import cv2
from cv2 import cv2
import pytesseract
from tkinter.filedialog import *
import os

pytesseract.pytesseract.tesseract_cmd='C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Ocr:
    def __init__(self, root):
        self.root = root
        self.root.title("Optical Character Recognition")
        self.root.geometry("700x350+320+100")
        self.root.configure(bg='#a6eef4')
        self.img=''
        self.fname2=''
        self.root.resizable(0,0)

        F1 = Frame(self.root,bg='#a6eef4')
        F1.place(x=30, y=30, width=600, height=50)
        Button(F1,width=18,text="Open Image",font=("arial", 13), bg="orange", bd=1, command=self.selectimg).grid(padx=15,pady=3,row=0, column=0)
        Button(F1,width=18,text="Run OCR",font=("arial", 13), bg="orange", bd=1, command=self.scan).grid(padx=15,pady=3,row=0, column=1)
        Button(F1,width=18,text="Copy to Clipboard",font=("arial", 13), bg="orange", bd=1, command=self.save).grid(padx=25,pady=3,row=0, column=2)
        #Button(F1,width=15,text="Open in Notepad",font=("arial", 13), bg="orange", bd=1, command=self.opennp).grid(padx=15,pady=3,row=0, column=3)
        
        F2 = Frame(self.root)
        F2.place(x=40, y=80, width=620, height=200)
        scroll_y = Scrollbar(F2, orient=VERTICAL)
        
        self.txtarea = Text(F2, font="arial 14", yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=1)
        
        F3 = Frame(self.root,bg='#a6eef4')
        F3.place(x=160, y=300, width=300, height=50)
        Button(F3,width=12,text="Close Image",font=("arial", 13), bg="orange", bd=1, command=self.imgclose).grid(padx=15,pady=3,row=0, column=0)
        Button(F3,width=12,text="Exit",font=("arial", 13), bg="orange", bd=1, command=self.exitwin).grid(padx=15,pady=3,row=0, column=1)
        
    def selectimg(self):
        self.txtarea.delete(1.0,END)
        self.img = askopenfilename(filetypes=[("Image files", ".png .jpg .gif .jpeg")])
        if self.img!='':
            self.img = cv2.imread(self.img)
            self.img = ResizeWithAspectRatio(self.img, width=700)
            cv2.imshow('Image',self.img) 

    def scan(self):
        if self.img=='':
            messagebox.showerror("Error","Image not selected")
        else:
            cv2.destroyWindow('Image')
            self.img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
            self.txtarea.insert(INSERT, pytesseract.image_to_string(self.img))
            #himg,wimg,a = self.img.shape
            boxes = pytesseract.image_to_data(self.img)
            for x,b in enumerate(boxes.splitlines()):
                if x!=0:
                    b = b.split()
                    if len(b)==12:
                        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
                        cv2.rectangle(self.img,(x,y),(w+x,h+y),(0,0,255),1)
                        cv2.putText(self.img,b[11],(x,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(50,50.255),1)
                        cv2.waitKey(30)
                        cv2.imshow('Image',self.img)

    def save(self):
        if self.txtarea.get(1.0,END)=='\n':
            messagebox.showerror("Error","Empty Text")
        else:
            self.root.clipboard_clear()
            strin = self.txtarea.get(1.0,END)
            self.root.clipboard_append(strin)

    def opennp(self):
        self.fname2 = askopenfilename(filetypes=[("Text file", ".txt")])
        if self.fname2!='':
            os.startfile(self.fname2)

    def imgclose(self):
        cv2.destroyWindow('Image')
    
    def exitwin(self):
        op = messagebox.askyesno("Exit", "Do you really want to exit?")
        if op > 0:
            self.root.destroy()
    
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter) 
        
if __name__ == '__main__':
    root = Tk()
    Ocr(root)
    root.mainloop()