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

        # Display link length
        self.len_lbl = Label(self.sideFrame,text='Link length: %0.2f' % self.network.E_lengths[edge] + ' km',
                             anchor='w',justify=LEFT)
        self.len_lbl.pack(side='top',anchor='w',fill='x')
        
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
        
        self.inv_list.pack(side='left',padx=5,pady=10,fill='x')
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
        self.maint_entry = Entry(self.subframe,textvariable=self.budget)
        self.maint_set_button = Button(self.subframe,text='Set',command=self.new_maint)

        self.maint_label.pack(side='left',anchor='w',fill='x')
        self.maint_entry.pack(side='left',anchor='w',fill='x')
        self.maint_set_button.pack(side='left',anchor='w',fill='x')

        # Set target capacity of the item
        self.target = StringVar()
        self.target_label = Label(self.subframe,text='Target Capacity (Mbps) :',anchor='w',justify=LEFT)
        self.target_set_button = Button(self.subframe,text='Set',command=self.new_target)
        self.target_entry = Entry(self.subframe,textvariable=self.target)

        self.target_set_button.pack(side='right',anchor='w',fill='x')
        self.target_entry.pack(side='right',anchor='w',fill='x')
        self.target_label.pack(side='right',anchor='w',fill='x')

        # Site object selector
        self.links = StringVar()
        self.links.set('Link slots: ')
        self.linkslots_title = Label(self.sideFrame2,textvariable=self.links,anchor='w',
                               justify=LEFT)
        self.linkslots_title.pack(side='top',anchor='w',fill='x')

        self.wireslots = StringVar()
        self.wireslots.set('Link slots: \n\n')
        self.wireslots_title = Label(self.sideFrame2,textvariable=self.wireslots,anchor='w',
                               justify=LEFT)
        self.wireslots_title.pack(side='top',anchor='w',fill='x')

        self.slots_list = Listbox(self.sideFrame2,height=15,selectmode='SINGLE')
        self.slots_list.pack(side='top',padx=20,pady=10,fill='both')
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
        self.inv_list.bind('<ButtonPress-1>', lambda x: self.get_maint())
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
        st = self.network.NodeLinkSlots(self.edge[0])
        en = self.network.NodeLinkSlots(self.edge[1])

        # Concantante a long string to set
        str1 = 'Radio Link slots: ' + '\n at ' + self.network.V_name[self.edge[0]]
        str1 = str1 + '  ' + str(st[0]) + ' / ' + str(st[2])
        str1 = str1 + '\n at ' + self.network.V_name[self.edge[1]]
        str1 = str1 + '  ' + str(en[0]) + ' / ' + str(en[2])

        str2 = 'Wired Connection Link slots: ' + '\n at ' + self.network.V_name[self.edge[0]]
        str2 = str2 + '  ' + str(st[1]) + ' / ' + str(st[3])
        str2 = str2 + '\n at ' + self.network.V_name[self.edge[1]]
        str2 = str2 + '  ' + str(en[1]) + ' / ' + str(en[3])

        self.wireslots.set(str2)
        self.links.set(str1)
        self.refresh_item()
        self.refresh_inv()
        

    def do_add(self):
        if self.inv_list.curselection():
            self.sel = int(self.inv_list.curselection()[0])
            item_toadd = self.inventory[self.sel]
            if item_toadd.type() == 'Radio' or item_toadd.type() == 'Wired':
                if item_toadd.GetMaxLength() >= self.network.E_lengths[self.edge]:
                    added = self.network.AddItemToEdge(self.edge,item_toadd)
                    if added:
                        self.inventory.pop(self.sel)
                        game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                        self.do_item_change()
                    else:
                        messagebox.showwarning('Warning',
                                               'Item was not added. There were no available slots at either the start or end node',
                                               parent=self.root)
                else:
                    messagebox.showwarning('Warning',
                                               'Item was not added. The maximum distance ' +  item_toadd.GetName() + ' can transmit is %0.2f' % item_toadd.GetMaxLength() + ' km. This link is %0.2f' % self.network.E_lengths[self.edge] + ' km long.',
                                               parent=self.root)
            else:
                messagebox.showwarning('Warning','You cannot add this type of item to a link. You must add either Radio or wired communication equipment to a link.',parent=self.root)

    def do_remove(self):
        if self.slots_list.curselection():
            self.sel = int(self.slots_list.curselection()[0])
            rem_item = self.network.E_items[self.edge][self.sel]
            rem = self.network.RemoveItemFromEdge(self.edge,self.sel)
            if rem:
                # Item removal was successful
                self.inventory.append(copy.deepcopy(rem_item))
                game.action_q.append(['inv',copy.deepcopy(self.inventory)])
                self.do_item_change()
            else:
                messagebox.showwarning('Warning.','Invalid request',parent=self.root)

    def new_maint(self):
        # Check which item is selected
        self.sel_item.SetMaintenance(float(self.budget.get()) / 24 / 7)
        self.get_maint()

    def new_target(self):
        # Check which item is selected
        if self.sel_item.type() == 'Radio' or self.sel_item.type() == 'Wired':
            self.sel_item.SetCapacity(float(self.target.get()) * 1000000)
            self.des.set(self.sel_item.GetInfo())
            

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
