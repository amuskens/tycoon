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
    def __init__(self,parent,inventory,node,gamenetwork):
        self.inventory = inventory
        self.elig_inv = []
        self.node = node
        self.network = gamenetwork

        # Define fonts
        BoldFont = font.Font(family='Arial', size=14, weight='bold')

        # Create window
        self.root = Toplevel(parent)
        self.root.wm_title('Edit build slots')
        self.root.resizable(FALSE,FALSE)

        # Deine frames for layout
        self.Frame = Frame(self.root)
        self.Frame.pack(side='top')

        self.title_lbl = Label(self.Frame,text='Edit build slots at ' + self.network.V_name[node],
                               anchor='w',font=BoldFont)
        self.title_lbl.pack(anchor='w')

        # Make frames on the sides
        self.sideFrame = Frame(self.Frame)
        self.sideFrame.pack(side='left',fill='x')

        self.sideFrame2 = Frame(self.Frame)
        self.sideFrame2.pack(side='right',fill='x')
        
        # Make an inventory list, and set up scrollbar
        self.inv_title = Label(self.sideFrame,text='Inventory',anchor='w',
                               justify=LEFT)
        self.inv_title.pack(side='top',anchor='w',fill='x')
        self.inv_list = Listbox(self.sideFrame,height=30,width=40,selectmode='ExTENDED')
        self.inv_list.pack(side='left',padx=0,pady=10,fill='x')
        self.inv_scroll = Scrollbar(self.sideFrame,orient=VERTICAL,
                                     command=self.inv_list.yview,width=20)
        self.inv_list.configure(yscrollcommand=self.inv_scroll.set)
        self.inv_scroll.pack(side='right',fill='both')
        self.refresh_inv()

        # Add a combobox to select the item at the node
        self.item_sel = StringVar()
        self.item_combobox = ttk.Combobox(self.sideFrame2,textvariable=self.item_sel,state='readonly')
        self.item_combobox.pack(side='top',fill='x')
        # add to teh combobox
        selectable = []
        for i in self.network.V_items[self.node]:
            selectable.append(i.GetName())
        
        self.item_combobox.configure(values = selectable)
        self.item_sel.set(selectable[0])

        # Description viewer
        self.subframe = Frame(self.sideFrame2,relief='sunken',border=1)
        self.subframe.pack(side='top',fill='x')
        
        self.des = StringVar()
        self.des.set('Item description:\n\n\n\n\n\n')
        self.des_lbl = Label(self.subframe,text='Item Description:',textvariable=self.des,anchor='w',justify=LEFT)
        self.des_lbl.pack(side='top',anchor='w',fill='both')


        # Site object selector
        self.linkslots_title = Label(self.sideFrame2,text='Link Slots: ',anchor='w',
                               justify=LEFT)
        self.linkslots_title.pack(side='top',anchor='w',fill='x')

        self.slots_title = Label(self.sideFrame2,text='Build Slots:',anchor='w',
                               justify=LEFT)
        self.slots_title.pack(side='top',anchor='w',fill='x')

        self.slots_list = Listbox(self.sideFrame2,height=15,width=40,selectmode='ExTENDED')
        self.slots_list.pack(side='top',padx=20,pady=10)


        # Standby
        self.refresh_des()

    def refresh_inv(self):
        self.inv_list.delete(0, END)
        # Fill the inventory list with eligible items
        for item in self.inventory:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN]' + temp
            self.inv_list.insert(END,temp)

    def refresh_des(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item = self.inventory[self.sel]
            self.des.set(item.GetInfo())
        elif self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            item = self.item.GetInventory()[self.sel]
            self.des.set(item.GetInfo())

        self.root.after(200,self.refresh_des)
