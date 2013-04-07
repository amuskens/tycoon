# This class instantiates a menu which will allow items to be 
# added to a node

from tkinter import *
from tkinter import ttk
import copy

from capital import *
from networkgraph import *
from subslotedit import *
import game

global refresh_flag
refresh_flag = False

class EditNode():
    def __init__(self,parent,inventory,nodeid,gamenetwork):
        self.inventory = inventory
        self.elig_inv = []
        self.node = nodeid
        self.network = gamenetwork

        # Create window
        self.root = Toplevel(parent)
        self.root.wm_title('Edit Network Node')
        self.root.resizable(FALSE,FALSE)

        # Deine frames for layout
        self.Frame = Frame(self.root)
        self.Frame.pack(side='top')

        self.title_lbl = Label(self.Frame,text='Edit Node: ',anchor='w')
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
        self.inv_title.pack(side='top',anchor='w')

        self.inv_list = Listbox(self.sideFrame,height=30,width=60,selectmode='ExTENDED')
        self.inv_list.pack(side='left',padx=5,pady=10)
        self.refresh_inv()

        self.scrollbar = Scrollbar(self.sideFrame,orient=VERTICAL,
                                   command=self.inv_list.yview)
        self.inv_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right',fill='y')

        # List of site objects
        self.site_title = Label(self.sideFrame2,
                                text='Assets at SIte' + '\n' + str(self.network.GetMaxSlots()) + ' total slots.',
                                anchor='w',
                                justify=LEFT)
        self.site_title.pack(side='top',anchor='w')

        self.subframe = Frame(self.sideFrame2,relief='sunken',border=1)
        self.subframe.pack(side='top',fill='x')
        
        self.des = StringVar()
        self.des.set('Item description:\n\n\n\n\n\n')
        self.des_lbl = Label(self.subframe,text='Item Description:',textvariable=self.des,anchor='w',justify=LEFT)
        self.des_lbl.pack(side='top',anchor='w',fill='both')

        self.site_list = Listbox(self.sideFrame2,height=10,width=40,selectmode='EXTENDED')
        self.site_list.pack(side='top',padx=20,pady=10)
        self.refresh_site()

        # Add and remove buttons

        self.button_add = Button(self.sideFrame2,
                                 text='Add from Inventory to Site',
                                 command=self.do_add)
        self.button_add.pack(side='top',fill='x')

        self.button_remove = Button(self.sideFrame2,
                                    text='Remove from Site to Inventory',
                                    command=self.do_remove)
        self.button_remove.pack(side='top',fill='x')

        # Close button
        self.button_close = Button(self.sideFrame2,
                                    text='Close',
                                    command=self.close)
        self.button_close.pack(side='top',fill='x')

        # Standby
        self.refresh_des()
        self.standby()
    

    def refresh_inv(self):
        self.inv_list.delete(0, END)
        # Fill the inventory list with eligible items
        for item in self.inventory:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN] ' + temp
            if not item.type() == 'Structure':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.inv_list.insert(END,temp)

    def refresh_site(self):
        self.site_list.delete(0,END)
        for item  in self.network.V_items[self.node]:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN] ' + temp
            if not item.type() == 'Structure':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.site_list.insert(END,temp)

    def do_add(self):
        if self.inv_list.curselection():
            for sel in self.inv_list.curselection():
                selected = int(sel)
                if self.inventory[selected].type() == 'Structure':
                    if len(self.network.V_items[self.node]) < self.network.GetMaxSlots():
                        self.network.V_items[self.node].append(copy.deepcopy(self.inventory[selected]))
                        self.inventory.pop(selected)
                        game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                        self.refresh_site()
                        self.refresh_inv()
                    else:
                        messagebox.showinfo('Warning','You cannot add more than ' + str(self.network.GetMaxSlots()) + ' items to this node.',
                                            parent=self.root)
                else:
                    messagebox.showinfo('Warning','Only strucutral items, such as buildings or towers can be added to a node.',parent=self.root)
                                      
    
    def do_remove(self):
        if self.site_list.curselection():
            for sel in self.site_list.curselection():
                selected = int(sel)
                item = copy.deepcopy(self.network.V_items[self.node].pop(selected))
                self.inventory.append(item)
                game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                self.refresh_site()
                self.refresh_inv()
                

    def close(self):
        self.root.destroy()


    def refresh_des(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item = self.inventory[self.sel]
            self.des.set(item.GetInfo())
        elif self.site_list.curselection():
            self.sel = int(self.site_list.curselection()[0])
            item = self.network.V_items[self.node][self.sel]
            self.des.set(item.GetInfo())

        self.root.after(200,self.refresh_des)
        
    def standby(self):
        global refresh_flag
        if refresh_flag:
            self.refresh_inv()
            refresh_flag = False
            
        self.root.after(500,self.standby)
