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
        self.inv_list = Listbox(self.sideFrame,height=30,width=60,selectmode='ExTENDED')
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
        # add to the combobox
        selectable = []
        for i in self.network.V_items[self.node]:
            selectable.append(i.GetName())
        
        self.item_combobox.configure(values = selectable)
        self.item_sel.set(selectable[0])
        self.item = self.network.V_items[self.node][0]
        self.item_combobox.bind('<<ComboboxSelected>>', lambda x: self.do_item_change())

        # Description viewer
        self.subframe = Frame(self.sideFrame2,relief='sunken',border=1)
        self.subframe.pack(side='top',fill='x')
        
        self.des = StringVar()
        self.des.set('Item description:\n\n\n\n\n\n')
        self.des_lbl = Label(self.subframe,text='Item Description:',textvariable=self.des,anchor='w',justify=LEFT)
        self.des_lbl.pack(side='top',anchor='w',fill='both')


        # Site object selector
        self.links = StringVar()
        self.links.set('Link slots: ')
        self.linkslots_title = Label(self.sideFrame2,textvariable=self.links,anchor='w',
                               justify=LEFT)
        self.linkslots_title.pack(side='top',anchor='w',fill='x')

        self.slots = StringVar()
        self.slots.set('Build slots: \n\n')
        self.slots_title = Label(self.sideFrame2,textvariable=self.slots,anchor='w',
                               justify=LEFT)
        self.slots_title.pack(side='top',anchor='w',fill='x')

        self.slots_list = Listbox(self.sideFrame2,height=15,width=40,selectmode='ExTENDED')
        self.slots_list.pack(side='top',padx=20,pady=10)
        
        # Buttons
        self.button_add = Button(self.sideFrame2,
                                 text='Add from Inventory to Build Slot',
                                 command=self.do_add)
        self.button_add.pack(side='top',fill='x')

        self.button_remove = Button(self.sideFrame2,
                                    text='Remove item from Build Slot',
                                    command=self.do_remove)
        self.button_remove.pack(side='top',fill='x')

        self.button_close = Button(self.sideFrame2,
                                   text='Close',
                                   command=self.close)
        self.button_close.pack(side='top',fill='x')


        # Standby
        self.refresh_des()
        self.refresh_item()
        self.do_item_change()

    # Close the window
    def close(self):
        self.root.destroy()

    def refresh_inv(self):
        self.inv_list.delete(0, END)
        # Fill the inventory list with eligible items
        for item in self.inventory:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN] ' + temp
            if item.type() == 'Structure' or item.type() == 'Radio' or item.type() == 'Wired':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.inv_list.insert(END,temp)

    def refresh_item(self):
        # Refreshes the listbox showing items in teh tower/building inventory
        self.slots_list.delete(0, END)
        for item in self.item.GetInventory():
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN] ' + temp
            if item.type() == 'Structure' or item.type() == 'Radio':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.slots_list.insert(END,temp)

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

    def do_item_change(self):
        self.item = self.network.V_items[self.node][self.item_combobox.current()]
        self.links.set('Link slots: ' + str(self.item.GetCurLinkSlots()) + ' / ' + str(self.item.GetMaxLinkSlots()))
        self.slots.set('Build slots: ' + str(len(self.item.GetInventory())) + ' / ' + str(self.item.slots) + '\n\nItems in build slots:')
        self.refresh_item()
        self.refresh_inv()
        

    def do_add(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item_toadd = self.inventory[self.sel]
            if not item_toadd.type() == 'Structure':
                if not (tem_toadd.type() == 'Wired' or item.toadd.type() = 'Radio'):
                    if self.item.AddItem(item_toadd):
                        # Successful add
                        self.inventory.pop(self.sel)
                        self.do_item_change()
                        game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                    else:
                        messagebox.showwarning('Warning',
                                               self.item.GetName() + ' has a full inventory. You cannot add '+ item_toadd.GetName(),
                                               parent=self.root)
                else:
                    messagebox.showwarning('Warning','You cannot add link assets to this site. Add link items to the links on the map',parent=self.root)
            else:
                messagebox.showwarning('Warning','You cannot add a structural type, like a building or tower, to an already existing building or tower.',parent=self.root)

    def do_remove(self):
        pass
