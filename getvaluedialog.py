
from tkinter import *
from tkinter import ttk

from capital import *

# This function  displays a dialog box which gets a value and returns
# it.

class  GetValueDialog():
    def __init__(self,parent,inString):
        self.result = None

        self.window = Toplevel(parent)
        self.window.wm_title('Enter a value:')
        self.window.lift()
        self.window.resizable(FALSE,FALSE)
    
        self.frame = Frame(self.window,relief='sunken',width=200,height=100)
        self.frame.grid(column=0,row=0,rowspan=3,columnspan=3)

        self.title = Label(self.frame,text='Enter a value for ' + inString)
        self.title.grid(column=0,row=0,rowspan=1,columnspan=2)
    
        # Use this special type to automatically update the variable value.
        self.getVal = StringVar()
        self.entryBox = Entry(self.frame,textvariable=self.getVal)
        self.entryBox.grid(column=0,row=1,rowspan=1,columnspan=3)

        self.applybutton = Button(self.frame,text='Apply',command=self.apply)
        self.applybutton.grid(column=1,row=3,columnspan=1,rowspan=1)

        self.cancelbutton = Button(self.frame,text='Cancel',command=self.close)
        self.cancelbutton.grid(column=2,row=3,columnspan=1,rowspan=1)

    def apply(self):
        self.result = float(self.getVal.get())
 

    def close(self):
        self.result = 0
        self.window.destroy()
                  
