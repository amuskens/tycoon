
from tkinter import *
from tkinter import ttk

class SubslotDisplay():
    def __init__(self):

        self.root = Tk()
        self.root.wm_title('Edit slots...')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame = Frame(self.root,relief='sunken',
                           width=640,
                           height=480)
        self.frame.grid(column=0, row=0, columnspan=3, rowspan=2)
