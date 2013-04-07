# This class allows you to edit building sub slots

from tkinter import *
from tkinter import ttk
import copy

from capital import *
from networkgraph import *
import game

global refresh_flag
refresh_flag = False

class EditSubslot():
    def __init__(self,parent,inventory,nodeid,gamenetwork,item):
        self.inventory = inventory
        self.elig_inv = []
        self.node = nodeid
        self.network = gamenetwork

        # Create window
        self.root = Toplevel(parent)
        self.root.wm_title('Edit ' + item.GetName() + ' build slots')
        self.root.resizable(FALSE,FALSE)

        # Deine frames for layout
        self.Frame = Frame(self.root)
        self.Frame.pack(side='top')

        self.title_lbl = Label(self.Frame,text='Edit build slots: ',anchor='w')
        self.title_lbl.pack(anchor='w')

        # Make frames on the sides
        self.sideFrame = Frame(self.Frame)
        self.sideFrame.pack(side='left')

        self.sideFrame2 = Frame(self.Frame)
        self.sideFrame2.pack(side='right')
        
        # Bottom frame for buttons
        self.bottomFrame = Frame(self.Frame)
        self.bottomFrame.pack(side='bottom')
        
        # Make an inventory list
        self.inv_title = Label(self.sideFrame,text='Inventory',anchor='w',
                               justify=LEFT)
        self.inv_title.pack(side='top',anchor='w',fill='x')

        self.inv_list = Listbox(self.sideFrame,height=40,width=40,selectmode='ExTENDED')
        self.inv_list.pack(side='top',padx=20,pady=10)
        self.refresh_inv()

        # Site object selector
        self.linkslots_title = Label(self.sideFrame,text='Build Slots',anchor='w',
                               justify=LEFT)
        self.linkslots_title.pack(side='top',anchor='w',fill='x')

        self.slots_title = Label(self.sideFrame,text='Build Slots',anchor='w',
                               justify=LEFT)
        self.slots_title.pack(side='top',anchor='w',fill='x')

        self.slots_list = Listbox(self.sideFrame,height=15,width=40,selectmode='ExTENDED')
        self.slots_list.pack(side='top',padx=20,pady=10)





    def refresh_inv(self):
        self.inv_list.delete(0, END)
        # Fill the inventory list with eligible items
        for item in self.inventory:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN]' + temp
            self.inv_list.insert(END,temp)
