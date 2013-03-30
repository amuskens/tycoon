
from tkinter import *
from tkinter import ttk

from capital import *

class SubslotDisplay():
    def __init__(self,items):
        # List of items comes in
        self.item_list = items

        # Create window
        self.root = Toplevel()
        self.root.wm_title('Edit slots...')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.frame = Frame(self.root,relief='sunken',
                           bd=5,width=640,height=480)

        self.frame.grid(column=0, row=0, columnspan=6, rowspan=15)

        self.title2_lbl = Label(self.frame,text='Select a component:',anchor='w')
        self.title2_lbl.grid(column=1,row=1,columnspan=1,rowspan=1)

        self.button_ok = Button(self.frame,text='OK',command=self.Ok)
        self.button_ok.grid(column=4,row=15,columnspan=2,rowspan=1)

        self.button_cancel = Button(self.frame,text='Cancel',command=self.close)
        self.button_cancel.grid(column=6,row=15,columnspan=2,rowspan=1)

        # Initialize the list box with items.
        phone = StringVar()
        
        text = []
        i = 0
        # Get text strings
        while i < 3:
            try:
                text.append(self.item_list[i].GetName())
            except:
                text.append('Empty Slot ' + str(i))
            i = i + 1

        print(text)

        self.slot1 = ttk.Radiobutton(self.frame, text=text[0], variable=phone, value='1')
        self.slot1.grid(column=0,row=2,columnspan=1,rowspan=1)
        self.slot2 = ttk.Radiobutton(self.frame, text=text[1], variable=phone, value='2')
        self.slot2.grid(column=0,row=3,columnspan=1,rowspan=1)
        self.slot3 = ttk.Radiobutton(self.frame, text=text[2], variable=phone, value='3')
        self.slot3.grid(column=0,row=4,columnspan=1,rowspan=1)
        
        self.itemselector = Listbox(self.frame,height=10)
        self.itemselector.grid(column=0,row=5,columnspan=2,rowspan=8)

        self.button_add = Button(self.frame,text='Add...')
        self.button_add.grid(column=0,row=14,columnspan=1,rowspan=1)

        self.button_remove = Button(self.frame,text='Remove')
        self.button_remove.grid(column=1,row=14,columnspan=1,rowspan=1)

    def Ok(self):
        self.close()

    def close(self):
        self.root.destroy()
        


        
