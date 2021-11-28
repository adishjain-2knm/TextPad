import tkinter as tk
from tkinter.messagebox import showinfo

class TextPad:
 
    __root = tk.Tk()
 
    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __TextArea = tk.Text(__root)
    __MenuBar = tk.Menu(__root)
    __temp1= tk.Menu(__MenuBar,tearoff=0)
    __temp2= tk.Menu(__MenuBar,tearoff=0)
    __temp3= tk.Menu(__MenuBar,tearoff=0)
    __temp4= tk.Menu(__MenuBar,tearoff=0)
    

    def __todo():
        showinfo("warning temp","To be implemented")

    __button = tk.Button(__root,text="this button",command=__todo)
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
        #self.__button.grid()
        self.__temp1.add_command(label="submenu button", command=self.__todo)
        self.__temp1.add_command(label="submenu button2", command=self.__todo)
        self.__temp1.add_command(label="submenu button3", command=self.__todo)
        

        self.__MenuBar.add_cascade(label="test1",menu=self.__temp1)
        self.__MenuBar.add_cascade(label="test1",menu=self.__temp2)
        self.__MenuBar.add_cascade(label="test1",menu=self.__temp3)
        self.__MenuBar.add_cascade(label="test1",menu=self.__temp4)
        
        self.__root.config(menu=self.__MenuBar)


        self.__TextArea.grid(sticky = tk.N + tk.E + tk.S +tk.W)            
 
    def __todo(self):
        showinfo("warning temp","To be implemented")

    def run(self):
        # Run main application
        self.__root.mainloop()
 

if __name__ == "__main__":
    textPad = TextPad(width=600,height=400)
    textPad.run()