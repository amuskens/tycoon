
from tkinter import *
from tkinter import ttk

class SubslotDisplay():
    def __init__(self):

        self.root = Toplevel()
        self.root.wm_title('Edit slots...')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame = Frame(self.root,relief='sunken',
                           width=640,
                           height=480)

        self.frame.grid(column=0, row=0, columnspan=3, rowspan=10)
        
        self.subFrame = Frame(self.frame,relief='sunken',
                              width=480,height=420)
        self.frame.grid(column=0, row=0, columnspan=2, rowspan=8)

        self.canvas = Canvas(self.subFrame,border=2)
        self.canvas.grid(column=0, row=0, columnspan = 2 , rowspan=9)

        self.button_ok = Button(self.frame,text='OK')
        self.button_ok.grid(column=0,row=0,columnspan=1,rowspan=1)

        self.button_ok = Button(self.frame,text='OK')
        self.button_ok.grid(column=3,row=10,columnspan=1,rowspan=1)


        
