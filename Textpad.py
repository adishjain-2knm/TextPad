import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    root.title("first window")
    l1 = tk.Label(root,text="This lable")
    l1.grid(row=0,column=0)
    root.mainloop()