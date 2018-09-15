# Used to easily start the program

import sys
sys.path.append("src")

import mp3_tags_gui as gui
from tkinter import Tk

if __name__ == "__main__":
    Window = Tk()
    GUI =  gui.MP3_Tags_GUI(Window)
    Window.mainloop()
