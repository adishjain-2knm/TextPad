import tkinter as tk

def halfscr():
    w,h= wind.winfo_screenwidth(),wind.winfo_screenheight()
    wind.geometry("%dx%d"%(w/2,h/2))
    wind.geometry(" 303x400 ")

def maxmized_window():
    wind.state("zoomed")  

if __name__ == "__main__":
    wind=tk.Tk()
    wind.title("This window")
    halfscr()

    maxmized_window()

    wind.mainloop()