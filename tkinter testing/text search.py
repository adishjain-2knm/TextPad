import tkinter as tk


if __name__ == "__main__":
    wind=tk.Tk()
    wind.title("This window")
    w2=tk.Tk()
    tx=tk.Text(w2)
    tx.grid(row=0,column=0)
    en=tk.Entry(wind)
    en.grid(row=0,column=0)

    def sf():
            tx.tag_remove('found','1.0',tk.END)
            tobe_search = en.get()
            idx=tx.index(tk.INSERT)
            if(tobe_search):
                print(idx)
            # searches for desired string from index 1
                i = tx.search(tobe_search, idx,stopindex = tk.END)
                print(i)
                if not i: i='1.0'
                
                # last index sum of current index and
                # length of text
                lastidx = '% s+% dc' % (i, len(tobe_search))
                
                tx.mark_set(tk.INSERT,lastidx)
                tx.tag_add('found', i, lastidx)
                i = lastidx
            tx.focus_set()
                    
    bt=tk.Button(wind,text='find',command=sf)
    bt.grid(row=0,column=1)
    wind.mainloop()