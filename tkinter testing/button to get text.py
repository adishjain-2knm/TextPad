import tkinter as tk

def halfscr():
    w,h= created_window.winfo_screenwidth(),created_window.winfo_screenheight()
    created_window.geometry("%dx%d"%(w/2,h/2))

def maxmized_window():
    created_window.state("zoomed")  


if __name__ == "__main__":
    created_window=tk.Tk()
    created_window.title("first window")
    halfscr()
    lab1=tk.Label(created_window,text="starting text")
    lab1.grid(row=0,column=0)
    tex1=tk.Entry(created_window)
    tex1.grid(row=1,column=0)
    tex1.focus()
    def fun_exected_when_pressed_button():
        text_typed_in_box = tex1.get()
        lab1.configure(text="text entered is : "+text_typed_in_box)
    but1=tk.Button(created_window,text="first button",command=fun_exected_when_pressed_button)
    but1.grid(row=3,column=0)
    created_window.mainloop()