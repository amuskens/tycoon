# This class allows you to edit building sub slots

from tkinter import *
from tkinter import ttk
import copy

from capital import *
from networkgraph import *
import game

global refresh_flag
refresh_flag = False

class EditLink():
    def __init__(self,parent,inventory,edge,gamenetwork):
        self.inventory = inventory
        self.elig_inv = []
        self.edge = edge
        self.network = gamenetwork

        # Define fonts
        BoldFont = font.Font(family='Arial', size=14, weight='bold')

        # Create window
        self.root = Toplevel(parent)
        self.root.wm_title('Edit Link')
        self.root.resizable(FALSE,FALSE)

        # Deine frames for layout
        self.Frame = Frame(self.root)
        self.Frame.pack(side='top')

        self.title_lbl = Label(self.Frame,text='Edit link from ' + self.network.V_name[edge[0]] + ' to ' + self.network.V_name[edge[1]],
                               anchor='w',font=BoldFont)
        self.title_lbl.pack(anchor='w')

        # Make frames on the sides
        self.sideFrame = Frame(self.Frame)
        self.sideFrame.pack(side='left',fill='x')

        self.sideFrame2 = Frame(self.Frame)
        self.sideFrame2.pack(side='right',fill='x')

        # DIsplay capacity of the link
        self.cap = StringVar()
        self.cap.set('Max Capacity of Link:')
        self.cap_lbl = Label(self.sideFrame,textvariable=self.cap,anchor='w',justify=LEFT)
        self.cap_lbl.pack(side='top',anchor='w',fill='x')
        
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
        self.slots.set('Link slots: \n\n')
        self.slots_title = Label(self.sideFrame2,textvariable=self.slots,anchor='w',
                               justify=LEFT)
        self.slots_title.pack(side='top',anchor='w',fill='x')

        self.slots_list = Listbox(self.sideFrame2,height=15,width=40,selectmode='SINGLE')
        self.slots_list.pack(side='top',padx=20,pady=10)
        self.slots_list.bind('<ButtonPress-1>', lambda x: self.get_maint())
        
        # Buttons
        self.button_add = Button(self.sideFrame2,
                                 text='Add from Inventory to Link',
                                 command=self.do_add)
        self.button_add.pack(side='top',fill='x')

        self.button_remove = Button(self.sideFrame2,
                                    text='Remove item from Link',
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
            if item.type() == 'Structure' or item.type() == 'Router':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.inv_list.insert(END,temp)

    def refresh_item(self):
        # Refreshes the listbox showing items in teh tower/building inventory
        self.slots_list.delete(0, END)
        for item in self.network.E_items[self.edge]:
            temp = item.GetName()
            if not item.Operating():
                temp = '[BROKEN] ' + temp
            if item.type() == 'Structure' or item.type() == 'Router':
                temp = temp + '  [INELIGIBLE ITEM]'
            self.slots_list.insert(END,temp)

    def refresh_des(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            self.sel_item = self.inventory[self.sel]
            self.des.set(self.sel_item.GetInfo())
        elif self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            self.sel_item = self.network.E_items[self.edge][self.sel]
            self.des.set(self.sel_item.GetInfo())

        # Refresh max capacity display
        self.cap.set('Maximum capacity available at link: %0.2f' % (self.network.MaxCapAtEdge(self.edge) / 1000000) + ' Mbps')

        self.root.after(200,self.refresh_des)

    def do_item_change(self):
        # self.links.set('Link slots: ' + str(self.item.GetCurLinkSlots()) + ' / ' + str(self.item.GetMaxLinkSlots()))
        # self.slots.set('Build slots: ' + str(len(self.item.GetInventory())) + ' / ' + str(self.item.slots) + '\n\nItems in build slots:')
        self.refresh_item()
        self.refresh_inv()
        

    def do_add(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item_toadd = self.inventory[self.sel]
            if item_toadd.type() == 'Radio' or item_toadd.type() == 'Wired':
                self.network.E_items[self.edge].append(copy.deepcopy(item_toadd))
                self.inventory.pop(self.sel)
                game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                self.do_item_change()
            else:
                messagebox.showwarning('Warning','You cannot add this type of item to a link. You must add either Radio or wired communication equipment to a link.',parent=self.parent)

    def do_remove(self):
        pass

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
            item = self.network.E_items[self.edge][self.sel]
            self.budget.set('%0.2f' % (item.GetMaintenance() * 24 * 7))
