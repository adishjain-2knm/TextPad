import tkinter as tk
import os   
#from tkinter import *
from tkinter import Label, font
from tkinter.constants import END, INSERT
from tkinter.messagebox import *
from tkinter.filedialog import *
from functools import partial

class TextPad:
 
    __root = tk.Tk()
 
    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __TextArea = tk.Text(__root,undo=True)
    __MenuBar = tk.Menu(__root)
    __FileMenu = tk.Menu(__MenuBar, tearoff=0)
    __EditMenu = tk.Menu(__MenuBar, tearoff=0)
    __FormatMenu = tk.Menu(__MenuBar,tearoff=0)
    __HelpMenu = tk.Menu(__MenuBar, tearoff=0)
    #__FontFamiltList = list(font.families())
    __CurrentFont = tk.StringVar(__root,'Arial')
    __CurrentFontSize = int('14')
    __FontDropSubmenu = tk.Menu(__FormatMenu,tearoff=0)
    __FontSizeSubmenu = tk.Menu(__FormatMenu,tearoff=0)

    # To add scrollbar
    __thisScrollBar = tk.Scrollbar(__TextArea)    
    __file = None
 
    def __init__(self,**kwargs):
 
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

        self.__EditMenu.add_separator()

        self.__EditMenu.add_command(label='Undo',accelerator='Ctrl+z',command=self.__undo)

        self.__EditMenu.add_command(label='Rndo',accelerator='Ctrl+y',command=self.__redo)

        self.__EditMenu.add_separator()

        self.__EditMenu.add_command(label="Find",accelerator='Ctrl+f',command=self.__find)

        self.__EditMenu.add_command(label="Replace",command=self.__findnReplace)
        

        # To give a feature of editing
        self.__MenuBar.add_cascade(label="Edit",
                                       menu=self.__EditMenu)    
        
        #self.__FontDrop = Menu(self.__FormatMenu,self.__CurrentFont,*self.__FontFamiltList,command=self.__formating)
        self.__FontDropSubmenu.add_command(label='Arial', command=partial(self.__ChangeFont,'Arial'))
        self.__FontDropSubmenu.add_command(label='Courier', command=partial(self.__ChangeFont,'Courier'))
        self.__FontDropSubmenu.add_command(label='Cambrier', command=partial(self.__ChangeFont,'Cambrier'))
        self.__FontDropSubmenu.add_command(label='Helvetica', command=partial(self.__ChangeFont,'Helvetica'))
        self.__FontDropSubmenu.add_command(label='Times', command=partial(self.__ChangeFont,'Times'))
        
        
        #self.__FormatMenu.add_cascade(label=f"{self.__CurrentFont}",menu=self.__FontDropSubmenu)
        self.__FormatMenu.add_cascade(label="Font List",menu=self.__FontDropSubmenu)

        self.__FontSizeSubmenu.add_command(label="12",command=partial(self.__ChangeFontSize,12))
        self.__FontSizeSubmenu.add_command(label="20",command=partial(self.__ChangeFontSize,20))
        self.__FontSizeSubmenu.add_command(label="30",command=partial(self.__ChangeFontSize,30))
        self.__FontSizeSubmenu.add_command(label="40",command=partial(self.__ChangeFontSize,40))

        self.__FormatMenu.add_cascade(label="Font Size",menu=self.__FontSizeSubmenu)
        
        self.__MenuBar.add_cascade(label="Format",menu=self.__FormatMenu)

        # To create a feature of description of the TextPad
        self.__HelpMenu.add_command(label="About TextPad",
                                        command=self.__showAbout)
        self.__MenuBar.add_cascade(label="Help",
                                       menu=self.__HelpMenu)

        self.__MenuBar.add_separator()

        self.__MenuBar.add_command(label="Bold",command=self.__bolder)
        
        self.__MenuBar.add_command(label="Italic",command=self.__italicer)

        #self.__MenuBar.add_command(label="Underline",command=self.__todo)


        

        self.__MenuBar.add_separator()

        #self.__MenuBar.add_command(label="OCR",command=self.__todo)
        
        self.__root.config(menu=self.__MenuBar)
 
        self.__thisScrollBar.pack(side=tk.RIGHT,fill=tk.Y)                   
         
        # Scrollbar will adjust automatically according to the content       
        self.__thisScrollBar.config(command=self.__TextArea.yview)    
        self.__TextArea.config(yscrollcommand=self.__thisScrollBar.set)
     
    def __todo(self):
        showinfo("warning temp","To be implemented")

    def __formating(self):
        self.__todo()
         
    def __quitApplication(self):
        self.__root.destroy()
        # exit()
 
    def __showAbout(self):
        showinfo("TextPad","Adish Jain")

    def __bolder(self):
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

    def __italicer(self):
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
         
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files","*.*"),
                                        ("Text Documents","*.txt")])
 
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
            self.__file = asksaveasfilename(initialfile='Untitled.txt',
                                            defaultextension=".txt",
                                            filetypes=[("All Files","*.*"),
                                                ("Text Documents","*.txt")])
 
            if self.__file == "":
                self.__file = None
            else:
                 
                # Try to save the file
                file = open(self.__file,"w")
                file.write(self.__TextArea.get(1.0,tk.END))
                file.close()
                 
                # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - TextPad")
                 
             
        else:
            file = open(self.__file,"w")
            file.write(self.__TextArea.get(1.0,tk.END))
            file.close()

    def __ChangeFont(self,Font_name:str):
        self.__CurrentFont=Font_name
        i=int(self.__CurrentFontSize)
        self.__TextArea.config(font=(Font_name,i))
    
    def __ChangeFontSize(self,FontSize:int):
        st=self.__CurrentFont
        self.__CurrentFontSize=FontSize
        self.__TextArea.config(font=(st,FontSize))
        #print(f"{st} {FontSize}")



    def __cut(self):
        self.__TextArea.event_generate("<<Cut>>")
        #print('cut called')
 
    def __copy(self):
        self.__TextArea.event_generate("<<Copy>>")
        #print('copy called')
 
    def __paste(self):
        self.__TextArea.event_generate("<<Paste>>")
        #print('paste called')
 
    def __undo(self):
        self.__TextArea.edit_undo()
        #print('undo called')

    def __redo(self):
        self.__TextArea.edit_redo()
        #print('redo called')

    def __find(self):
        __wind = tk.Tk()
        __wind.geometry("200x100")
        __find_lab = tk.Label(__wind,text='Find : ')
        __find_lab.grid(row=0,column=0)
        __find_box=tk.Entry(__wind)
        __find_box.grid(row=0,column=1)
        
        def sf():
            idx=self.__TextArea.index(INSERT)
            self.__TextArea.tag_remove(tk.SEL,'1.0',END)
            tobe_search = __find_box.get()
            print(self.__TextArea.get('1.0',END))
            print(tobe_search)
            if(tobe_search):
                
            # searches for desired string from index 1
                print(idx)
                i = self.__TextArea.search(tobe_search, idx,stopindex = END)
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

        __find_button = tk.Button(__wind,text="find now",command=sf)
        __find_button.grid(row=1,column=0,columnspan=2)

    def __findnReplace(self):
        __wind = tk.Tk()
        __wind.title('Find and Replace')
        __wind.geometry("200x100")
        __find_lab = tk.Label(__wind,text='Find : ')
        __find_lab.grid(row=0,column=0)
        __find_box=tk.Entry(__wind)
        __find_box.grid(row=0,column=1)
        __replace_lab = tk.Label(__wind,text='replace : ')
        __replace_lab.grid(row=1,column=0)
        __replace_box=tk.Entry(__wind)
        __replace_box.grid(row=1,column=1)
        

        idx=self.__TextArea.index(INSERT)
        def sf(idx):
            self.__TextArea.tag_remove('found','1.0',END)
            tobe_search = __find_box.get()
            if(tobe_search):
                
            # searches for desired string from index 1
                    print(idx)
                    idx = self.__TextArea.search(tobe_search, idx, nocase = 1,
                                    stopindex = END)
                    print(idx)
                    if not idx: idx='1.0'
                    
                    # last index sum of current index and
                    # length of text
                    lastidx = '% s+% dc' % (idx, len(tobe_search))
                    
                    self.__TextArea.mark_set(tk.INSERT,idx)

        
                    # overwrite 'Found' at idx
                    self.__TextArea.tag_add('found', idx, lastidx)
                    idx = lastidx
                    print(idx)

        __find_button = tk.Button(__wind,text="Replace",command=partial(sf,idx))
        __find_button.grid(row=2,column=0,columnspan=2)  

    def run(self):
 
        # Run main application
        self.__root.mainloop()
 
 
 
if __name__ == "__main__":
# Run main application
    textPad = TextPad(width=600,height=400)
    textPad.run()