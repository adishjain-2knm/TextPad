import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    wind=tk.Tk()
    wind.config(background="red")
    wind.grid_columnconfigure((0),weight=1)
    # wind.grid_rowconfigure((0,1),weight=1)
    notebool_tabs = ttk.Notebook(wind)
    notebool_tabs.grid(row=0,sticky="EW")
    #notebool_tabs.grid_columnconfigure(0,weight=1)

    option1 = tk.Label(wind,text="option1")
    option1.grid(row=1,sticky="E")
    option2 = tk.Label(wind,text="option2")
    option2.grid(row=1,sticky="W")
    option3 = tk.Label(wind,text="option3")
    option3.grid(row=1,sticky="E")
    option4 = tk.Label(wind,text="option4")
    option4.grid(row=1,sticky="E")
    
    
    notebool_tabs.add(option1,text="menu 1")
    notebool_tabs.add(option2,text="menu 2")
    notebool_tabs.add(option3,text="menu 3")
    notebool_tabs.add(option4,text="menu 4")
    areas=tk.Text(wind)
    areas.grid(row=3,column=0)
    
    wind.mainloop()
