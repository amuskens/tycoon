
from tkinter import *
from tkinter import ttk

from capital import *
from database import *
import game

global refresh_flag
refresh_flag = False

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

        # Deine frames for layout
        self.topFrameRoot = Frame(self.root)
        self.topFrameRoot.pack(side='top')

        self.topFrame = Frame(self.topFrameRoot)
        self.topFrame.pack(side='left')

        self.topFrame2 = Frame(self.topFrameRoot)
        self.topFrame2.pack(side='right')

        self.topFrame3 = Frame(self.topFrame2,relief='sunken',border=1,width=300)
        self.topFrame3.pack(side='top')

        self.frame = Frame(self.root)
        self.frame.pack(side='left')

        self.sideframe = Frame(self.root)
        self.sideframe.pack(side='right')

        self.bottomFrame = Frame(self.root)
        self.bottomFrame.pack(side='bottom')

        # Define labels
        self.title_lbl = Label(self.topFrame,text='Telecom Equipment Store:',anchor='w')
        self.title_lbl.pack(anchor='w')

        self.cat_lbl = Label(self.topFrame,text='Category:',anchor='w')
        self.cat_lbl.pack(anchor='w')


        # Define object type radio buttons
        self.v = StringVar()
        self.v.set("tower") # initialize

        self.rad1 = Radiobutton(self.topFrame,text='Towers',variable=self.v,value='tower',anchor='w')
        self.rad1.pack(side='top',fill='x',padx=20)
        self.rad1.select()
        self.rad2 = Radiobutton(self.topFrame,text='Buildings',variable=self.v,value='building',anchor='w')
        self.rad2.pack(side='top',fill='x',padx=20)
        self.rad3 = Radiobutton(self.topFrame,text='Routers',variable=self.v,value='router',anchor='w')
        self.rad3.pack(side='top',fill='x',padx=20)
        self.rad4 = Radiobutton(self.topFrame,text='Radios',variable=self.v,value='radio',anchor='w')
        self.rad4.pack(side='top',fill='x',padx=20)
        self.rad5 = Radiobutton(self.topFrame,text='Wired Point to Point',variable=self.v,value='wire',anchor='w')
        self.rad5.pack(side='top',fill='x',padx=20)

        # Define object description label
        self.des = StringVar()
        self.des.set('Item description:\n\n\n\n\n\n')
        self.des_lbl = Label(self.topFrame3,text='Item Description:',textvariable=self.des,anchor='w',justify=LEFT)
        self.des_lbl.pack(side='left',anchor='w')

        self.catsel_lbl = Label(self.frame,text='Items in Category:',anchor='w')
        self.catsel_lbl.pack(anchor='w',pady=10)

        self.invsel_lbl = Label(self.sideframe,text='Items in Inventory:',anchor='w')
        self.invsel_lbl.pack(anchor='w',pady=10)


        # Select item list boxes
        self.itemselector = Listbox(self.frame,height=40,width=40,selectmode=SINGLE)
        self.itemselector.pack(side='top',padx=20,pady=10)
        self.refresh_descrip_sel()

        self.inv_select = Listbox(self.sideframe,height=40,width=40,selectmode=BROWSE)
        self.inv_select.pack(side='top',padx=20,pady=10)
        self.refresh_descrip_inv()
        self.refresh_inv()

        # Action buttons
        self.button_add = Button(self.bottomFrame,text='Add... >',command=self.do_add)
        self.button_add.pack(side='top',fill='x')

        self.button_remove = Button(self.bottomFrame,text='Remove from inventory...',
                                    command=self.do_remove)
        self.button_remove.pack(side='top',fill='x')

        self.button_ref = Button(self.bottomFrame,text='Refresh Inventory',
                                    command=self.refresh_inv)
        self.button_ref.pack(side='top',fill='x')

        self.button_close = Button(self.bottomFrame,text='Close',command=self.close)
        self.button_close.pack(side='right',fill='x')

        # Set up radio buttons to refresh automatically when changed
        self.v.trace("w", lambda name, index, mode: self.refresh_catlist())
        self.refresh_catlist()

        # Standby
        self.standby()

    def refresh_catlist(self):
        self.itemselector.delete(0, END)

        # Check to see what was changed.
        if self.v.get() == 'tower':
            for item in self.database.Towers.keys():
                self.itemselector.insert(END,self.database.GetTower(item).GetName())

        elif self.v.get() == 'building':
            for item in self.database.Buildings.keys():
                self.itemselector.insert(END,self.database.Buildings[item][0])

        elif self.v.get() == 'radio':
            for item in self.database.Radios.keys():
                self.itemselector.insert(END,self.database.GetRadio(item).GetName())

        elif self.v.get() == 'router':
            for item in self.database.Routers.keys():
                self.itemselector.insert(END,self.database.GetRouter(item).GetName())

        elif self.v.get() == 'wire':
            for item in self.database.Wired.keys():
                self.itemselector.insert(END,self.database.GetWired(item).GetName())

    def refresh_inv(self):
        self.inv_select.delete(0, END)
        for item in self.inventory:
            self.inv_select.insert(END,item.GetName())

    def refresh_descrip_sel(self):
        if self.itemselector.curselection():
            sel = int(self.itemselector.curselection()[0])

            # Handle each object type differently
            if self.v.get() == 'tower':
                item = self.database.GetTower(sel)
                tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
                tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
                tempstr = tempstr + '\nFoundation Cost: $ %0.2f' % float(item.GetFoundationCost())
                tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
                tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
                tempstr = tempstr + '\nTower Type: ' + item.GetTowerType()
                tempstr = tempstr + '\nTower Height: ' + item.GetTowerHeight() + ' m'
                tempstr = tempstr + '\nBuild slots: ' + str(item.slots)
                
                self.sel_item = item
                self.des.set(tempstr)
            elif self.v.get() == 'building':
                item = self.database.GetBuilding(sel)
                tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
                tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
                tempstr = tempstr + '\nFoundation Cost: $ %0.2f' % float(item.GetFoundationCost())
                tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
                tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
                tempstr = tempstr + '\nBuild slots: ' + str(item.slots)
                self.sel_item = item
                self.des.set(tempstr)

            elif self.v.get() == 'radio':
                item = self.database.GetRadio(sel)
                tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
                tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
                tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
                tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
                tempstr = tempstr + '\nMaximum Capacity: %0.2f' % (float(item.GetMaxCapacity()) / 1000000) + ' megabits per second'
                tempstr = tempstr + '\nMaximum Link Length: ' + str(item.GetMaxLength()) + ' km'
                tempstr = tempstr + '\nFrequency Range: %0.2f' % (float(item.GetFreqRange()[0])) + ' MHz to %0.2f' % (float(item.GetFreqRange()[1])) + ' MHz'
                tempstr = tempstr + '\nRadio Type: ' + item.RadioGetType()
                self.sel_item = item
                self.des.set(tempstr)

            elif self.v.get() == 'wire':
                item = self.database.GetWired(sel)
                tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
                tempstr = tempstr + '\nCost per km: $ ' + "%0.2f" % item.GetCost() + ' / km'
                tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
                tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
                tempstr = tempstr + '\nOptimal Maximum Capacity: %0.2f' % (float(item.GetMaxCapacity()) / 1000000) + ' megabits per second'
                tempstr = tempstr + '\nMaximum Link Length: ' + str(item.GetMaxLength()) + ' km'
                tempstr = tempstr + '\nCapacity for 1 km: %0.2f' % (float(item.DistCapacity(1) / 1000000)) + ' megabits per second'
                tempstr = tempstr + '\nAttenuation: %0.2f' % (float(item.GetAttenuation()) / 100) + ' dB'
                tempstr = tempstr + '\nType: ' + item.WiredGetType()
                self.sel_item = item
                self.des.set(tempstr)
                
        self.itemselector.after(250,self.refresh_descrip_sel)

    def refresh_descrip_inv(self):
        if self.inv_select.curselection():
            self.inv_sel = int(self.inv_select.curselection()[0])

            item = self.inventory[self.inv_sel]

            tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
            tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
            tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
            tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
            tempstr = tempstr + '\nAge: %0.0f' % (item.GetAge()) + ' hours, or %0.2f' % (item.GetAge() / 365 / 24) + ' years'

            self.des.set(tempstr)

        self.inv_select.after(200,self.refresh_descrip_inv)
        
    def do_add(self):
        if self.sel_item:
            self.inventory.append(self.sel_item)
            cost = self.sel_item.GetCost()
            if self.sel_item.type() == 'Structure':
                cost = cost + float(self.sel_item.GetFoundationCost())
            game.action_q.append(['subtractcash',[cost]])
            self.refresh_inv()

    def do_remove(self):
        if self.inv_select.curselection():
            self.inv_sel = int(self.inv_select.curselection()[0])
            answer = messagebox.askquestion('Question',
                                   'Are you sure you wish to remove this item from the inventory? You cannot recover the cost.')

            if answer: 
                self.inventory.pop(self.inv_sel)
                self.refresh_inv()
            
            

    def Ok(self):
        self.close()

    def close(self):
        self.root.destroy()

    # This method is called when the window idles.
    def standby(self):
        global refresh_flag
        if refresh_flag:
            self.refresh_inv()
            refresh_flag = False
            
        self.root.after(500,self.standby)
        
        


        
