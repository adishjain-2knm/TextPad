import tkinter as tk

def halfscr():
    w,h= first_window.winfo_screenwidth(),first_window.winfo_screenheight()
    first_window.geometry("%dx%d"%(w/2,h/2))

def maxmized_window():
    first_window.state("zoomed")  


if __name__ == "__main__":
    first_window=tk.Tk()
    first_window.title("first window")
    halfscr()
    lab1=tk.Label(first_window,text="starting text")
    lab1.grid(row=0,column=1)
    def fun_exected_when_pressed_button():
        lab1.configure(text="%d , %d "%(first_window.winfo_width(),first_window.winfo_height()))

    but1=tk.Button(first_window,text="first button",command=fun_exected_when_pressed_button)
    but1.grid(row=0,column=0)
    first_window.mainloop()
