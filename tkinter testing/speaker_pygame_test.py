
from tkinter import *
import pyttsx3
import pygame

pygame.mixer.init()
engine = pyttsx3.init()

root = Tk()

def read():
    outfile = "temp.wav"
    engine.save_to_file(text.get('1.0', END), outfile)
    engine.runAndWait()
    pygame.mixer.music.load(outfile)
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def pause():
    pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()


text = Text(width=65, height=20, font="consolas 14")
text.pack()

text.insert(END, "This is a text widget\n"*10)

read_button = Button(root, text="Read aloud", command=read)
read_button.pack(pady=20)

pause_button = Button(root, text="Pause", command=pause)
pause_button.pack()

unpause_button = Button(root, text="Unpause", command=unpause)
unpause_button.pack(pady=20)

stop_button = Button(root, text="Stop", command=stop)
stop_button.pack()

mainloop()