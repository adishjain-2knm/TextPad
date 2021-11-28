import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk

class TextPad:
 
    __root = tk.Tk()
    __root.config(background="red")
    
    # default window width and height
    __thisWidth = 300
    __thisHeight = 300
    __TextArea = tk.Text(__root)
    __notebool_tabs = ttk.Notebook(__root)
    __notebool_tabs.grid(row=0,sticky="EW")
    __option1 = tk.Label(__root,text="option1")
    __option1.grid(row=1,sticky="E")
    __option2 = tk.Label(__root,text="option2")
    __option2.grid(row=1,sticky="W")
    __option3 = tk.Label(__root,text="option3")
    __option3.grid(row=1,sticky="E")
    __option4 = tk.Label(__root,text="option4")
    __option4.grid(row=1,sticky="E")

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
        self.__notebool_tabs.add(self.__option1,text="menu 1")
        self.__notebool_tabs.add(self.__option2,text="menu 2")
        self.__notebool_tabs.add(self.__option3,text="menu 3")
        self.__notebool_tabs.add(self.__option4,text="menu 4")

        self.__TextArea.grid(sticky = tk.N + tk.E + tk.S +tk.W)            
 
    def run(self):
        # Run main application
        self.__root.mainloop()
 

if __name__ == "__main__":
    textPad = TextPad(width=600,height=400)
    textPad.run()