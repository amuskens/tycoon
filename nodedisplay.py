# Defines an object which is a small window 
# which displays information about a node.

from tkinter import *

from game import *
from capital import *
from database import *
from networkgraph import *
from subslotedit import *

import random

class NodeDisplay():
    def __init__(self,x,y,canvas,node_num,networkgraph,imagedict):
        # Set initial parameters
        x = canvas.canvasx(x)
        y = canvas.canvasy(y)
        self.x = x
        self.y = y
        self.width = 450
        self.height = 160
        self.canvas = canvas
        self.node = node_num
        self.network = networkgraph
        self.id = random.randint(1,1000)

        Font1 = font.Font(family='Arial', size=14, weight='bold')
        Font2 = font.Font(family='Helvetica', size=12, weight='bold')
        Font3 = font.Font(family='Arial', size=12)

        # Start by drawing the interface
        self.window = self.canvas.create_rectangle(x,y,x+self.width,y+self.height,
                                                   fill='white',activefill='white',
                                                   outline='white',tags=str(self.id))
        
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
        counter = 0
        
        # Add the items from the slots.
        while counter < self.network.max_slots:
            self.slot_obj.append(self.canvas.create_rectangle(x,y + 45 + voffset,x + self.width,y + 72 + voffset,
                                                              fill='gray',outline='gray',tags=str(self.id)))
            try:
                item = self.network.V_items[self.node][counter]
            except:
                item = None
            if item:
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

                self.canvas.tag_bind(a,"<ButtonPress-1>", lambda x: self.subslots(counter))

                self.slot_text.append(self.canvas.create_text(x+15, y + 56 + voffset,
                                                              text=item.StructType(),
                                                              fill='black',
                                                              anchor='nw',
                                                              font=Font3,
                                                              tags=str(self.id)))
                self.slot_text.append(self.canvas.create_text(x+140,y + 45 + voffset,
                                                              text=('Maintennace Budget:   $ ' + str(item.GetMaintenance())),
                                                              fill='black',activefill='blue',anchor='nw',font=Font3,tags=str(self.id)))
                self.slot_text.append(self.canvas.create_text(x+140,y + 57 + voffset,
                                                              text=('Suggested  Budget: $ ' + str(item.SugMaintenance())),
                                                              fill='black',anchor='nw',font=Font3,tags=str(self.id)))

                # Test age
                if item.OverLifespan():
                    temp = 'Replace. Over Lifespan'
                    fillcolor='red'
                else:
                    temp = 'Within Lifespan'
                    fillcolor='green'

                self.slot_text.append(self.canvas.create_text(x+330,y + 45 + voffset,
                                                              text='Age: ' + str(item.GetAge()),
                                                              fill=fillcolor,anchor='nw',font=Font2,tags=str(self.id)))
                self.slot_text.append(self.canvas.create_text(x+330,y + 57 + voffset,
                                                              text=temp,
                                                              fill=fillcolor,anchor='nw',font=Font2,tags=str(self.id)))
            else:
                self.slot_text.append(self.canvas.create_text(x+15,y + 45 + voffset,
                                                              text='<Empty slot>',
                                                              fill='black',activefill='blue',anchor='nw',font=Font3,tags=str(self.id)))
            voffset = voffset + 30
            counter = counter + 1


        # Draw close button and attach event
        self.closebutton = self.canvas.create_image(x + self.width - 16,
                                                    y + 10,
                                                    image=imagedict['close'],
                                                    activeimage=imagedict['close_active'],tags=str(self.id))

        self.canvas.tag_bind(self.closebutton,"<Button-1>", lambda x: self.close())
    
    # Close
    def close(self):
        self.canvas.delete(self.closebutton)
        for i in self.titles: self.canvas.delete(i)
        for i in self.slot_text: self.canvas.delete(i)
        for i in self.slot_obj: self.canvas.delete(i)
        self.canvas.delete(self.window)

    # Drag window
    def drag(self,event):
        pass

    # Select items in subslot
    def subslots(self,item_index):
        new = SubslotDisplay()
        
