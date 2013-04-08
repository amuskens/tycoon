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

        # Display node cap
        self.cap = StringVar()
        self.cap.set('Max Capacity of Node:')
        self.cap_lbl = Label(self.Frame,textvariable=self.cap,anchor='w',justify=LEFT)
        self.cap_lbl.pack(side='top',anchor='w',fill='x')

        self.capset = StringVar()
        self.capset.set('Used Capacity of Node:')
        self.capset_lbl = Label(self.Frame,textvariable=self.capset,anchor='w',justify=LEFT)
        self.capset_lbl.pack(side='top',anchor='w',fill='x')

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
        self.inv_list.bind('<ButtonPress-1>', lambda x: self.get_maint())
        self.inv_list.pack(side='left',padx=0,pady=10,fill='x')
        self.inv_scroll = Scrollbar(self.sideFrame,orient=VERTICAL,
                                     command=self.inv_list.yview,width=20)
        self.inv_list.configure(yscrollcommand=self.inv_scroll.set)
        self.inv_scroll.pack(side='right',fill='both')
        self.refresh_inv()

        # Add a combobox to select the item at the node
        self.sel_title = Label(self.sideFrame2,text='Selectable Node Items:',anchor='w',
                               justify=LEFT)
        self.sel_title.pack(side='top',anchor='w',fill='x')
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

        # Allow setting of maintenance budget for items.
        self.budget = StringVar()
        self.maint_label = Label(self.subframe,text='Current Weekly Maintenance Budget:  $',anchor='w',justify=LEFT)
        self.maint_label.pack(side='left',anchor='w',fill='x')

        self.maint_set_button = Button(self.subframe,text='Set',command=self.new_maint)
        self.maint_set_button.pack(side='right',anchor='w',fill='x')

        self.maint_entry = Entry(self.subframe,textvariable=self.budget)
        self.maint_entry.pack(side='right',anchor='w',fill='x')

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
        self.slots_list.bind('<ButtonPress-1>', lambda x: self.get_maint())
        
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
            self.sel_item = self.inventory[self.sel]
            self.des.set(self.sel_item.GetInfo())
        elif self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            self.sel_item = self.item.GetInventory()[self.sel]
            self.des.set(self.sel_item.GetInfo())

        self.cap.set('Maximum capacity available at Node: %0.2f' % (self.network.MaxCapAtNode(self.node) / 1000000) + ' Mbit/s')
        self.capset.set('Current Used capacity available at node: %0.2f' % (self.network.cap_at_node_cached[self.node] / 1000000) + ' Mbit/s')    

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
                if not (item_toadd.type() == 'Wired' or item_toadd.type() == 'Radio'):
                    if self.item.AddItem(item_toadd):
                        # Successful add
                        self.inventory.pop(self.sel)
                        self.do_item_change()
                        game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                    else:
                        # Not so successful. Must be full.
                        messagebox.showwarning('Warning',
                                               self.item.GetName() + ' has a full inventory. You cannot add '+ item_toadd.GetName(),
                                               parent=self.root)
                else:
                    messagebox.showwarning('Warning','You cannot add link assets to this site. Add link items to the links on the map',parent=self.root)
            else:
                messagebox.showwarning('Warning','You cannot add a structural type, like a building or tower, to an already existing building or tower.',parent=self.root)

    def do_remove(self):
        if self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            item_toremove = self.item.RemoveItem(self.sel)
            self.inventory.append(copy.deepcopy(item_toremove))
            self.do_item_change()
            game.action_q.append(['inv',copy.deepcopy(self.inventory)])

    def new_maint(self):
        # Check which item is selected
            self.sel_item.SetMaintenance(float(self.budget.get()) / 24 / 7)
            self.get_maint()

    def get_maint(self):
        # Check which item is selected
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item = self.inventory[self.sel]
            self.budget.set('%0.2f' % (item.GetMaintenance() * 24 * 7))
        elif self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            item = self.item.GetInventory()[self.sel]
            self.budget.set('%0.2f' % (item.GetMaintenance() * 24 * 7))
