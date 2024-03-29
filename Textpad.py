import tkinter as tk
import os   

from tkinter import font
from tkinter.messagebox import *
from tkinter.filedialog import *
from functools import partial
from tkinter import colorchooser

import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import ocr_A
import pyttsx3
import pygame

class TextPad:
 
    __root = tk.Tk()        # main root  window
 
    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    
    __CurrentFont = tk.StringVar(__root,'Times')
    __CurrentFontSize = int('28')
    __TextArea = tk.Text(__root,font=(__CurrentFont,__CurrentFontSize),undo=True)
    __MenuBar = tk.Menu(__root)
    __FileMenu = tk.Menu(__MenuBar, tearoff=0)
    __EditMenu = tk.Menu(__MenuBar, tearoff=0)
    __FormatMenu = tk.Menu(__MenuBar,tearoff=0)
    __HelpMenu = tk.Menu(__MenuBar, tearoff=0)
    __StyleMenu = tk.Menu(__MenuBar,tearoff=0)
    __FontDropSubmenu = tk.Menu(__FormatMenu,tearoff=0)
    __FontSizeSubmenu = tk.Menu(__FormatMenu,tearoff=0)
    
    #module for text to speach
    __Text2SpeechRate= int(120)
    __t2s_module = None
    
    __thisScrollBar = tk.Scrollbar(__TextArea)    
    __file = None
    __tempMenu=tk.Menu(__root,tearoff=0)
    
    def __init__(self,**kwargs):

        self.__root.bind_all("<Control-f>", self.__find)
        self.__root.bind_all("<Control-r>", self.__findnReplace)
        self.__root.bind_all("<Control-b>", self.__bolder)
        self.__root.bind_all("<Control-i>", self.__italicer)
        self.__t2s_module = pyttsx3.init()
        self.__t2s_module.setProperty('rate',120)
        self.__Text2SpeechRate = int(120)
        # Set icon
        try:
                self.__root.wm_iconbitmap("TextPad.ico")
        except:
                pass
 
        # Set window size (the default is 300x300)
 
        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass
 
        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass
    
        # Set the window text
        self.__root.title("Untitled - TextPad")
 
        # Center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
     
        # For left-align
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        #self.left
         
        # For right-align
        top = (screenHeight / 2) - (self.__thisHeight /2)
         
        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
                                              self.__thisHeight,
                                              left, top))
 
        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
 
        # Add controls (widget)
        self.__TextArea.grid(sticky = tk.N + tk.E + tk.S +tk.W)

        #self.__create_icons()
         
        # To open new file
        self.__FileMenu.add_command(label="New",
                                        command=self.__newFile)   
         
        # To open a already existing file
        self.__FileMenu.add_command(label="Open",
                                        command=self.__openFile)
        
        # To save current file
        self.__FileMenu.add_command(label="Save",
                                        command=self.__saveFile)   
 
        # To create a line in the dialog       
        self.__FileMenu.add_separator()                                        
        self.__FileMenu.add_command(label="Exit",
                                        command=self.__quitApplication)
        self.__MenuBar.add_cascade(label="File",
                                       menu=self.__FileMenu)    
         
        # To give a feature of cut
        self.__EditMenu.add_command(label="Cut",accelerator='Ctrl+x',
                                        command=self.__cut)            
     
        # to give a feature of copy   
        self.__EditMenu.add_command(label="Copy",accelerator='Ctrl+c',
                                        command=self.__copy)        
         
        # To give a feature of paste
        self.__EditMenu.add_command(label="Paste",accelerator='Ctrl+v',
                                        command=self.__paste)        

        #Following section contains Edit menu and its functionality
        self.__EditMenu.add_separator()
        self.__EditMenu.add_command(label='Undo',accelerator='Ctrl+z',command=self.__undo)
        self.__EditMenu.add_command(label='Rndo',accelerator='Ctrl+y',command=self.__redo)
        self.__EditMenu.add_separator()
        self.__EditMenu.add_command(label="Find",accelerator='Ctrl+f',command=self.__find)
        self.__EditMenu.add_command(label="Replace",accelerator='Ctrl+r',command=self.__findnReplace)

        # adding EditMenu to Main Menu
        self.__MenuBar.add_cascade(label="Edit",menu=self.__EditMenu)    

        # Generation of list of font 
        font_list=['Arial','Courier','Cambrier', 'Franklin Gothic Medium', 'Gabriola','Helvetica','Impact', 'Ink Free', 'Lucida Console','Papyrus','Times']
        for font in font_list:
            self.__FontDropSubmenu.add_command(label=font, command=partial(self.__ChangeFont,font))
        self.__FormatMenu.add_cascade(label="Font List",menu=self.__FontDropSubmenu)

        # Generation of list of font size
        font_sizes=[11,12,14,16,20,24,28,32,38,48,60,72]
        for size in font_sizes:
            self.__FontSizeSubmenu.add_command(label=str(size),command=partial(self.__ChangeFontSize,size))
        self.__FormatMenu.add_cascade(label="Font Size",menu=self.__FontSizeSubmenu)
        
        self.__MenuBar.add_cascade(label="Format",menu=self.__FormatMenu)

        # To create a feature of description of the TextPad
        self.__HelpMenu.add_command(label="About TextPad", command=self.__showAbout)

        #Style Menu for font color and styling
        self.__MenuBar.add_cascade(label="Help", menu=self.__HelpMenu)
        self.__MenuBar.add_separator()
        self.__StyleMenu.add_command(label="Bold",accelerator='Ctrl+b',command=self.__bolder)
        self.__StyleMenu.add_command(label="Italic",accelerator='Ctrl+i',command=self.__italicer)
        self.__StyleMenu.add_separator()
        self.__StyleMenu.add_command(label='Text Color',command=self.__ChangeTextColor)
        self.__StyleMenu.add_command(label='BG Color',command=self.__ChangeBGColor)
        self.__MenuBar.add_cascade(label="Style", menu=self.__StyleMenu)
        
        self.__MenuBar.add_separator()
        self.__MenuBar.add_separator()

        #adding option of Encryption in Main Menu
        self.__MenuBar.add_command(label="Encpt/Decrpt",command=self.__Encrypter)
        self.__MenuBar.add_separator()

        #Adding oprion of Optical Character Recognition to MainMenu
        self.__MenuBar.add_command(label="OCR",command=self.__OCR)
        self.__MenuBar.add_separator()

        #Adding Text To Speach Option
        self.__MenuBar.add_command(label='Text to Speach',command=self.__Text2Speach_wind)

        self.__root.config(menu=self.__MenuBar)
        self.__thisScrollBar.pack(side=tk.RIGHT,fill=tk.Y)                   
         
        # Scrollbar will adjust automatically according to the content       
        self.__thisScrollBar.config(command=self.__TextArea.yview)    
        self.__TextArea.config(yscrollcommand=self.__thisScrollBar.set)

    def __todo(self):
        showinfo("warning temp","To be implemented")
         
    def __quitApplication(self):
        self.__root.destroy()
 
    def __showAbout(self):
        showinfo("TextPad","Adish Jain, Suraj Prakash, Aaryan")

    def __bolder(self,event=None):
        bold_font= font.Font(self.__TextArea,self.__TextArea.cget("font"))
        bold_font.configure(weight="bold")
        self.__TextArea.tag_configure("bold", font=bold_font)
        try:
            bold_tags = self.__TextArea.tag_names("sel.first")
            if "bold" in bold_tags:
                self.__TextArea.tag_remove("bold","sel.first","sel.last")
            else:
                self.__TextArea.tag_add("bold","sel.first","sel.last")
        except tk.TclError:
            pass

    def __italicer(self,event=None):
        bold_font= font.Font(self.__TextArea,self.__TextArea.cget("font"))
        bold_font.configure(slant="italic")
        self.__TextArea.tag_configure("italic", font=bold_font)
        try:
            bold_tags = self.__TextArea.tag_names("sel.first")
            if "italic" in bold_tags:
                self.__TextArea.tag_remove("italic","sel.first","sel.last")
            else:
                self.__TextArea.tag_add("italic","sel.first","sel.last")
        except tk.TclError:
            pass

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt", filetypes=[("All Files","*.*"), ("Text Documents","*.txt")])
        if self.__file == "":
            # no file to open
            self.__file = None
        else:
            # Try to open the file
            # set the window title
            self.__root.title(os.path.basename(self.__file) + " - TextPad")
            self.__TextArea.delete(1.0,tk.END)
            file = open(self.__file,"r")
            self.__TextArea.insert(1.0,file.read())
            file.close()
         
    def __newFile(self):
        self.__root.title("Untitled - TextPad")
        self.__file = None
        self.__TextArea.delete(1.0,tk.END)
 
    def __saveFile(self):
        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                # Try to save the file
                file = open(self.__file,"w")
                file.write(self.__TextArea.get(1.0,tk.END))
                file.close()                
                self.__root.title(os.path.basename(self.__file) + " - TextPad")     # Change the window title
        else:
            file = open(self.__file,"w")
            file.write(self.__TextArea.get(1.0,tk.END))
            file.close()

    def __ChangeFont(self,Font_name:str):
        self.__CurrentFont=Font_name
        i=int(self.__CurrentFontSize)
        self.__TextArea.config(font=(Font_name,i))
        self.__bolder()
        self.__italicer()
    
    def __ChangeFontSize(self,FontSize:int):
        st=self.__CurrentFont
        self.__CurrentFontSize=FontSize
        self.__TextArea.config(font=(st,FontSize))
        self.__bolder()
        self.__italicer()

    def __cut(self):
        self.__TextArea.event_generate("<<Cut>>")
 
    def __copy(self):
        self.__TextArea.event_generate("<<Copy>>")
 
    def __paste(self):
        self.__TextArea.event_generate("<<Paste>>")
 
    def __undo(self):
        self.__TextArea.edit_undo()

    def __redo(self):
        self.__TextArea.edit_redo()

    def __ChangeTextColor(self):
        color_code = colorchooser.askcolor()
        self.__TextArea.config(foreground=color_code[1])

    def __ChangeBGColor(self):
        color_code = colorchooser.askcolor()
        self.__TextArea.config(background=color_code[1])

    def __find(self,event=None):            
        """Create Dialog Box to find a given subString in __TextArea"""
        __wind = tk.Tk()
        __wind.geometry("300x200")
        __find_lab = tk.Label(__wind,text='Find : ')
        __find_lab.grid(row=0,column=0)
        try:
            __sel_st=self.__TextArea.selection_get()
        except:
            __sel_st=''
        print(__sel_st)
        __find_box=tk.Entry(__wind)
        __find_box.insert(tk.END,__sel_st)
        __find_box.grid(row=0,column=1)
        def Text_find():
            idx=self.__TextArea.index(tk.INSERT)
            self.__TextArea.tag_remove(tk.SEL,'1.0',tk.END)
            tobe_search = __find_box.get()
            print(self.__TextArea.get('1.0',tk.END))
            print(tobe_search)
            if(tobe_search):
            # searches for desired string from index 1
                print(idx)
                i = self.__TextArea.search(tobe_search, idx,stopindex = tk.END)
                print(idx,i)
                if not i:
                    i=self.__TextArea.search(tobe_search, '1.0',stopindex = idx)
                if not i:
                    showinfo('warning','not found!')
                    return
                lastidx = '% s+% dc' % (i, len(tobe_search))
                self.__TextArea.mark_set(tk.INSERT,lastidx)
                self.__TextArea.tag_add(tk.SEL, i, lastidx)
                print(idx,i,' * ')
                __wind.destroy()
        __find_button = tk.Button(__wind,text="find now",command=Text_find)
        __find_button.grid(row=1,column=0,columnspan=2)


    def __findnReplace(self,event=None):
        __wind = tk.Tk()
        __wind.title('Find and Replace')
        __wind.geometry("300x250")
        __find_lab = tk.Label(__wind,text='Find : ')
        __find_lab.grid(row=0,column=0)
        try:
            __sel_st=self.__TextArea.selection_get()
        except:
            __sel_st=''
        __find_box=tk.Entry(__wind)
        __find_box.insert(tk.END,__sel_st)
        __find_box.grid(row=0,column=1)
        __replace_lab = tk.Label(__wind,text='replace : ')
        __replace_lab.grid(row=1,column=0)
        __replace_box=tk.Entry(__wind)
        __replace_box.grid(row=1,column=1)
        
        def Text_find_replace():
            idx=self.__TextArea.index(tk.INSERT)
            self.__TextArea.tag_remove(tk.SEL,'1.0',tk.END)
            tobe_search = __find_box.get()
            replace_with = __replace_box.get()
            print(self.__TextArea.get('1.0',tk.END))
            print(tobe_search)
            if(tobe_search and replace_with):
                # searches for desired string from index 1
                print(idx)
                i = self.__TextArea.search(tobe_search, idx,stopindex = tk.END)
                print(idx,i)
                if not i:
                    i=self.__TextArea.search(tobe_search, '1.0',stopindex = idx)
                if not i:
                    showinfo('warning','not found!')
                    return
                lastidx = '% s+% dc' % (i, len(tobe_search))
                self.__TextArea.delete(i,lastidx)
                self.__TextArea.insert(i,replace_with)
                lastrep = '% s+% dc' % (i, len(replace_with))
                
                self.__TextArea.mark_set(tk.INSERT,lastrep)
                self.__TextArea.tag_add(tk.SEL, i, lastrep)
                print(idx,i,' * ')
                __wind.destroy()
            else:
                if not replace_with :
                    showinfo("warning", "enter replaceing text")
                else:
                    showinfo('warning','Enter text to find')

        __find_button = tk.Button(__wind,text="find and replace",command=Text_find_replace)
        __find_button.grid(row=2,column=0,columnspan=2)

    def __Encrypter(self):          
        """Function to encrypt given text"""
        __wind = tk.Toplevel()
        __wind.focus_set()          #setting Encrypter dialogBox as "model window"
        __wind.grab_set()
        __wind.title('Encrypt')
        __wind.geometry("300x150")
        __pass_lab = tk.Label(__wind,text='Password : ')
        __pass_lab.grid(padx=20,pady=20,row=0,column=0)
        __pass_inp = tk.Entry(__wind,show='*')
        __pass_inp.grid(padx=20,pady=20,row=0,column=1)
        def enc():
            """Helper function for __Encrypt"""
            password = __pass_inp.get()
            print(password)
            if not password:
                showerror("Alert","Enter password")
                return
            self.encrypt(password,True)
        def dnc():
            """Helper function for __Encrypt"""
            password = __pass_inp.get()
            print(password)
            if not password:
                showerror("Alert","Enter password")
                return
            self.encrypt(password,False)
        __pass_btn1=tk.Button(__wind,text='enc me',command=enc,width=10,bg='cyan3')
        __pass_btn1.grid(padx=20,pady=20,row=1,column=0)
        __pass_btn=tk.Button(__wind,text='dnc me',command=dnc,width=10,bg='cyan3')
        __pass_btn.grid(padx=20,pady=20,row=1,column=1)

    def encrypt(self,pas,forwar=True):
        pas_byte= pas.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=bytes(1),
            iterations=10000,
            backend=default_backend()
        )
        key =kdf.derive(pas_byte)
        print(base64.urlsafe_b64encode(key))
        cipher_text=str()
        plain_text = self.__TextArea.get("1.0","end-1c")
        if(forwar):
            key=str(key)+plain_text
            for i in range(len(plain_text)):
                x= ( ord(plain_text[i]) ^ ord(key[i]) )
                cipher_text=cipher_text+chr(x)
        else:
            key = str(key)
            for i in range(len(plain_text)):
                x= ( ord(plain_text[i]) ^ ord(key[i]) )
                cipher_text=cipher_text+chr(x)
                key=key+(chr(x))
        self.__TextArea.delete("1.0","end-1c")
        self.__TextArea.insert('1.0',cipher_text)

    def __OCR(self):                    
        """OCR from Helper file"""
        __wind = tk.Tk()
        ocr_A.Ocr(__wind)

    def __Text2Speach_wind(self):       
        """create dialogBox for Text to Speach functionality"""
        __wind = tk.Toplevel()
        __wind.title("Text to Speach")
        __wind.geometry("400x300")
        pygame.mixer.init()             #pygame.mixer for audio playback

        f1=tk.Frame(__wind,bg="#b6eef4")
        f2=tk.Frame(__wind,bg="#a6eef4")
        f3=tk.Frame(__wind,bg="#86def4")

        f1.place(width=400,height=100)
        f2.place(y=100,width=400,height=100)
        f3.place(y=200,width=400,height=100)
        def updateRate(vr):
            self.__t2s_module.setProperty('rate',rateSelected.get())
            self.__Text2SpeechRate = rateSelected.get()
        
        rateOption=list(range(80,261,20))
        rateSelected = tk.IntVar()
        rateSelected.set(self.__Text2SpeechRate)
        rateMenu = tk.OptionMenu(f2,rateSelected,*rateOption,command=updateRate)
        rateMenu.config(width=18)

        def readAll():
            pygame.mixer.music.unload()
            if os.path.exists("speak.wav"):
                os.remove("speak.wav")
            outputFile = "speak.wav" 
            self.__t2s_module.save_to_file(self.__AllText(),outputFile)     #Creating wav file for playback
            self.__t2s_module.runAndWait()
            pygame.mixer.music.load(outputFile)
            pygame.mixer.music.play()

        def readSelected():
            pygame.mixer.music.unload()
            outputFile = "speak.wav"
            self.__t2s_module.save_to_file(self.__SelectedText(),outputFile)
            self.__t2s_module.runAndWait()
            pygame.mixer.music.load(outputFile)
            pygame.mixer.music.play()

        def stop():
            pygame.mixer.music.stop()
        def pause():
            pygame.mixer.music.pause()
        def unpause():
            pygame.mixer.music.unpause()
        playAllButton = tk.Button(f1,width=14,height=2,text="Speak all text",command=readAll)
        playAllButton.grid(padx=30,pady=10,row=0,column=0)
        playSelectedButton = tk.Button(f1,width=14,height=2,text="Speak selected text",command=readSelected)
        playSelectedButton.grid(padx=30,pady=10,row=0,column=1)

        labe = tk.Label(f2,width=14,height=2,text='Rate of Speach:')
        labe.grid(padx=30,pady=10,row=0,column=0)
        rateMenu.grid(padx=15,pady=10,row=0,column=1)

        playBtn=tk.Button(f3,width=14,height=2,text="Play",command=unpause)
        playBtn.grid(padx=15,pady=10,row=0,column=0)
        pauseBtn=tk.Button(f3,width=14,height=2,text="Pause",command=pause)
        pauseBtn.grid(padx=15,pady=10,row=0,column=1)
        stopBtn=tk.Button(f3,width=14,height=2,text="Stop",command=stop)
        stopBtn.grid(padx=15,pady=10,row=0,column=2)

    def __AllText(self):                                    
        """Helper function to get all text fron __TextArea"""
        str_to_speak = self.__TextArea.get(1.0,tk.END)
        return str_to_speak

    def __SelectedText(self):                               
        """Helper function of T2S to get only selected text from __TextArea"""
        if self.__TextArea.tag_ranges("sel"):
            str_to_speak= self.__TextArea.get("sel.first","sel.last")
            return str_to_speak
        return ""

    def run(self):                  #Start main loop
        self.__root.mainloop()
  
if __name__ == "__main__":
    textPad = TextPad(width=800,height=450)
    textPad.run()