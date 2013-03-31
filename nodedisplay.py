# Defines an object which is a small window 
# which displays information about a node.

from tkinter import *
import copy

from game import *
from capital import *
from database import *
from networkgraph import *
from subslotedit import *
from getvaluedialog import *

import random

class NodeDisplay():
    def __init__(self,x,y,canvas,node_num,networkgraph,imagedict,parent):
        # Set initial parameters
        self.x = x
        self.y = y
        self.width = 480
        self.height = 200
        self.canvas = canvas
        self.node = node_num
        self.network = networkgraph
        self.id = random.randint(1,1000)
        self.parent = parent
        self.imagedict = imagedict
        self.closed = False

        # Use a dictionary to get slot index from ID
        self.slot_dict = { }
        self.slot_maint_dict = { }

        Font1 = font.Font(family='Arial', size=14, weight='bold')
        Font2 = font.Font(family='Helvetica', size=12, weight='bold')
        Font3 = font.Font(family='Arial', size=12)

        # Start by drawing the interface
        self.window = self.canvas.create_rectangle(x,y,x+self.width,y+self.height,
                                                   fill='white',activefill='white',
                                                   outline='white',tags=str(self.id))
        self.canvas.tag_bind(self.window,"<ButtonPress-1>", lambda x: self.close())
        
        # Draw the parameters
        self.titles = []
        self.titles.append( self.canvas.create_text(x+5,y+3,
                                                    text=self.network.V_name[self.node],
                                                    fill='black',anchor='nw',font=Font1,
                                                    tags=str(self.id)))

        self.titles.append(self.canvas.create_line(x,y+20,x + self.width,
                                                   y+20,fill='black',
                                                   tags=str(self.id)))

        self.titles.append(self.canvas.create_text(x+5,y+25,
                                                   text="Slots:",
                                                   fill='black',anchor='nw',font=Font2,tags=(str(self.id))))
        self.slot_text = []
        self.slot_obj = []

        voffset = 0
        
        # Add the items from the slots.
        for item  in self.network.V_items[self.node]:
            self.slot_obj.append(self.canvas.create_rectangle(x,y + 45 + voffset,x + self.width,y + 82 + voffset,
                                                              fill='gray',outline='gray',tags=str(self.id)))
            if item.Operating(): 
                fillcolor = 'green'
            else: 
                fillcolor = 'red'

            self.slot_obj.append(self.canvas.create_rectangle(x+2,y+46+voffset,
                                                              x + 12,y + 55 + voffset,
                                                              fill=fillcolor,outline=fillcolor,tags=str(self.id)))

                
                

            a = (self.canvas.create_text(x+15,y + 45 + voffset,
                                         text=item.GetName(),
                                         fill='black',
                                         activefill='blue',
                                         anchor='nw',
                                         font=Font2,
                                         tags=str(self.id)))

            self.slot_text.append(a)
            self.canvas.tag_bind(a,"<ButtonPress-1>", lambda x: self.subslots(item))


            if item.StructType() == 'Tower':
                temp = str(item.GetTowerType()) + ' Tower' + '\n' + str(item.GetTowerHeight()) + ' m'
            else:
                temp = item.StructType()

            self.slot_text.append(self.canvas.create_text(x+15, y + 56 + voffset,
                                                          text=temp,
                                                          fill='black',
                                                          anchor='nw',
                                                          font=Font3,
                                                          tags=str(self.id)))

            # Special for attaching mouse event
            maint = self.canvas.create_text(x+180,y + 45 + voffset,
                                            text=('Maintennace Budget:   $ ' + str(item.GetMaintenance())),
                                            fill='black',activefill='blue',anchor='nw',font=Font3,tags=str(self.id))
            
            self.slot_text.append(maint)
            self.bindMouseRelease(maint,item)

                
            self.slot_text.append(self.canvas.create_text(x+180,y + 57 + voffset,
                                                          text=('Suggested  Budget: $ ' + str(item.SugMaintenance())),
                                                          fill='black',anchor='nw',font=Font3,tags=str(self.id)))

            # Test age
            if item.OverLifespan():
                temp = 'Replace.'
                fillcolor='red'
            else:
                temp = 'Within Lifespan'
                fillcolor='green'

            self.slot_text.append(self.canvas.create_text(x+380,y + 45 + voffset,
                                                              text='Age: ' + str(item.GetAge()),
                                                              fill=fillcolor,anchor='nw',font=Font2,tags=str(self.id)))
            self.slot_text.append(self.canvas.create_text(x+380,y + 57 + voffset,
                                                              text=temp,
                                                              fill=fillcolor,anchor='nw',font=Font2,tags=str(self.id)))
            voffset = voffset + 42


        # Draw an add button
        self.addbutton = self.canvas.create_image(x + self.width - 64,
                                                    y + self.height,
                                                    image=imagedict['addbutton'],
                                                    activeimage=self.imagedict['addbutton_active'],tags=str(self.id))

        self.canvas.tag_bind(self.addbutton,"<Button-1>", lambda x: self.close())

        # Draw close button and attach event
        self.closebutton = self.canvas.create_image(x + self.width - 16,
                                                    y + 10,
                                                    image=imagedict['close'],
                                                    activeimage=self.imagedict['close_active'],tags=str(self.id))

        self.canvas.tag_bind(self.closebutton,"<Button-1>", lambda x: self.close())
    # Close
    def close(self):
        self.canvas.delete(self.closebutton)
        for i in self.titles: self.canvas.delete(i)
        for i in self.slot_text: self.canvas.delete(i)
        for i in self.slot_obj: self.canvas.delete(i)
        self.canvas.delete(self.window)
        self.canvas.delete(self.addbutton)
        self.closed = True

    # Refresh ,x,y,canvas,node_num,networkgraph,imagedict,parent):
    def refresh(self):
        self.close()
        self.__init__(self.x,self.y,self.canvas,self.node,self.network,self.imagedict,self.parent)
        self.closed = False

    def Closed(self):
        return self.closed

    # Drag window
    def drag(self,event):
        pass

    # Select items in subslot
    def subslots(self,node):
        display  = SubslotDisplay(self.network.V_items[node])

    def GetMaint(self,item):
        self.msg_box('Set maintenance budget for ' + item.GetName() + '\nat ' +  self.network.V_name[self.node])
        self.item_to_change = item

    def msg_box(self, msg='?', extra=True):
        top = self.top = Toplevel(self.parent)
        top.resizable(FALSE,FALSE)
        label0 = Label(top, text=msg)
        label0.grid(column=0,row=0,columnspan=2,rowspan=2)

        if extra:
            self.entry0 = Entry(top)
            self.entry0.grid(column=0,row=2,rowspan=1,columnspan=3)

            button2 = Button(top, text='Set', command=self.submit_name)
            button2.grid(column=0,row=3,rowspan=1,columnspan=1)

        button3 = Button(top, text='Cancel',
                                command=lambda: self.top.destroy())
        button3.grid(column=2,row=3,rowspan=1,columnspan=1)

    def bindMouseRelease(self,shape,item):
        self.canvas.tag_bind(shape,"<ButtonPress-1>", lambda x: self.GetMaint(item))

    def submit_name(self):
        data = self.entry0.get()
        if data:
            self.item_to_change.SetMaintenance(data)
            self.top.destroy()
            self.refresh()

        
        
