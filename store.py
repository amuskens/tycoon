
from tkinter import *
from tkinter import ttk

from capital import *
from database import *

class Store():
    def __init__(self,parent,inventory,database):
        self.inventory = inventory
        self.database = database

        # Create window
        self.root = Toplevel(parent)
        self.root.wm_title('Store')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE,FALSE)

        self.topFrameRoot = Frame(self.root)
        self.topFrameRoot.pack()

        self.topFrame = Frame(self.topFrameRoot)
        self.topFrame.pack(side='left')

        self.topFrame2 = Frame(self.topFrameRoot)
        self.topFrame2.pack(side='right')

        self.frame = Frame(self.root)
        self.frame.pack(side='left')

        self.sideframe = Frame(self.root)
        self.sideframe.pack(side='right')

        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side='bottom')

        self.title_lbl = Label(self.topFrame,text='Telecom Equipment Store:',anchor='w')
        self.title_lbl.pack(anchor='w')

        self.cat_lbl = Label(self.topFrame,text='Category:',anchor='w')
        self.cat_lbl.pack(anchor='w')

        self.v = StringVar()
        self.v.set("L") # initialize

        self.rad1 = Radiobutton(self.topFrame,text='Towers',variable=self.v,value='tower',anchor='w')
        self.rad1.pack(side='top',fill='x',padx=20)
        self.rad1.select()
        self.rad2 = Radiobutton(self.topFrame,text='Buildings',variable=self.v,value='building',anchor='w')
        self.rad2.pack(side='top',fill='x',padx=20)
        self.rad3 = Radiobutton(self.topFrame,text='Routers',variable=self.v,value='router',anchor='w')
        self.rad3.pack(side='top',fill='x',padx=20)
        self.rad4 = Radiobutton(self.topFrame,text='Radios',variable=self.v,value='radio',anchor='w')
        self.rad4.pack(side='top',fill='x',padx=20)
        self.rad5 = Radiobutton(self.topFrame,text='Wired Point to Point',variable=self.v,value='wired',anchor='w')
        self.rad5.pack(side='top',fill='x',padx=20)

        self.catsel_lbl = Label(self.frame,text='Items in Category:',anchor='w')
        self.catsel_lbl.pack(anchor='w',pady=10)

        self.invsel_lbl = Label(self.sideframe,text='Items in Inventory:',anchor='w')
        self.invsel_lbl.pack(anchor='w',pady=10)

        self.itemselector = Listbox(self.frame,height=20,width=20)
        self.itemselector.pack(side='top',padx=20,pady=10)

        self.inv_select = Listbox(self.sideframe,height=20,width=20)
        self.inv_select.pack(side='top',padx=20,pady=10)

        self.button_add = Button(self.bottomFrame,text='Add...',command=self.refresh_catlist)
        self.button_add.pack(side='top',fill='x')

        self.button_remove = Button(self.bottomFrame,text='Remove')
        self.button_remove.pack(side='top',fill='x')

        self.button_close = Button(self.bottomFrame,text='Close',command=self.close)
        self.button_close.pack(side='right',fill='x')

        # Set up radio buttons to refresh automatically when changed
        self.v.trace("w", lambda name, index, mode: self.refresh_catlist())
        self.refresh_catlist()

    def refresh_catlist(self):
        self.itemselector.delete(0, END)

        # Check to see what was changed.
        if self.v.get() == 'tower':
            for item in self.database.Towers.keys():
                self.itemselector.insert(END,self.database.GetTower(item).GetName() + '\t\t\t $  ' + str(self.database.GetTower(item).GetCost()))

        elif self.v.get() == 'building':
            for item in self.database.Buildings.keys():
                self.itemselector.insert(END,self.database.GetBuilding(item).GetName())

        elif self.v.get() == 'radio':
            for item in self.database.Radios.keys():
                self.itemselector.insert(END,self.database.GetRadio(item).GetName())

    def refresh_inv(self):
        pass

    def Ok(self):
        self.close()

    def close(self):
        self.root.destroy()
        


        
