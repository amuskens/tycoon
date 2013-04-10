# Defines a submenu for the canvas accessed by right click

from tkinter import *
import copy

import game
from game import *
from capital import *
from database import *
from networkgraph import *
from subslotedit import *
from getvaluedialog import *
from distfuncs import dist

global LeftCounter

class CanvasSubMenu():
    def __init__(self,x,y,canvas,nodeorlink,imagedict,nodeflag=0,linkflag=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.imagedict = imagedict

        if nodeflag:
            self.node = nodeorlink
        elif linkflag:
            self.link = nodeorlink
        
        # Define some fonts
        Font1 = font.Font(family='Arial', size=14, weight='bold')
        Font2 = font.Font(family='Helvetica', size=12, weight='bold')
        Font3 = font.Font(family='Arial', size=12)

        # The nodeflag tells whether or not a node was clicked on.
        self.nodeflag = nodeflag
        self.linkflag = linkflag

        # Begin by drawing the submenu
        # Depending on whether a node was clicked, adding and deleting links should be disabled.
        # There are different combinations of iamgery for inactive icons, depening on the nodeflag
        if nodeflag == 1:
            image1 = self.imagedict['addlink']
            image2 = self.imagedict['addlink_active']
            image3 = self.imagedict['dellink_inactive']
            image4 = self.imagedict['dellink_inactive']
            image5 = self.imagedict['addnode_inactive']
            image6 = self.imagedict['addnode_inactive']
            image7 = self.imagedict['delnode']
            image8 = self.imagedict['delnode_active']
        elif linkflag == 1:
            image1 = self.imagedict['addlink_inactive']
            image2 = self.imagedict['addlink_inactive']
            image3 = self.imagedict['dellink']
            image4 = self.imagedict['dellink_active']
            image5 = self.imagedict['addnode']
            image6 = self.imagedict['addnode_active']
            image7 = self.imagedict['delnode_inactive']
            image8 = self.imagedict['delnode_inactive']
        else:
            image1 = self.imagedict['addlink_inactive']
            image2 = self.imagedict['addlink_inactive']
            image3 = self.imagedict['dellink_inactive']
            image4 = self.imagedict['dellink_inactive']
            image5 = self.imagedict['addnode']
            image6 = self.imagedict['addnode_active']
            image7 = self.imagedict['delnode_inactive']
            image8 = self.imagedict['delnode_inactive']

        # Draw buttons and bind mouse events
        self.addlink = canvas.create_image(x + 200,y,
                                           image=image1,
                                           activeimage=image2,
                                           anchor='nw')
        self.canvas.tag_bind(self.addlink,"<ButtonPress-1>", lambda x: self.do_addlink())
        
        self.dellink = canvas.create_image(x + 300,y,
                                           image=image3,
                                           activeimage=image4,
                                           anchor='nw')
        self.canvas.tag_bind(self.dellink,"<ButtonPress-1>", lambda x: self.do_dellink())

        self.addnode = canvas.create_image(x,y,
                                           image=image5,
                                           activeimage=image6,
                                           anchor='nw')
        self.canvas.tag_bind(self.addnode,"<ButtonPress-1>", lambda x: self.do_addnode())

        self.delnode = canvas.create_image(x + 100,y,
                                           image=image7,
                                           activeimage=image8,
                                           anchor='nw')
        self.canvas.tag_bind(self.delnode,"<ButtonPress-1>", lambda x: self.do_delnode())

        self.closebutton = canvas.create_image(x + 400,y,
                                               image=self.imagedict['close'],
                                               activeimage=self.imagedict['close_active'],
                                               anchor='center')
        self.canvas.tag_bind(self.closebutton,"<ButtonPress-1>", lambda x: self.close())

        """
        The idea is to use a global action stack to pass
        the operations done back to the game class so the game
        class can update the graphics in the next step.

        """
    def close(self):
        self.canvas.delete(self.addlink)
        self.canvas.delete(self.addnode )
        self.canvas.delete(self.delnode)
        self.canvas.delete(self.dellink)
        self.canvas.delete(self.closebutton)

    def do_addlink(self):
        if self.nodeflag:
            # Wait until
            game.clicked = False
            self.canvas.bind("<Double-Button-1>", lambda x: self.returnCoord())
            self.close()
            self.selected = self.canvas.create_oval(self.x -30,self.y -30,self.x + 30,self.y + 30,
                                       outline='red',width=3)

                
    def returnCoord(self):
        game.action_q.append(['addlink',[self.node,
                                             (self.canvas.canvasx(game.lastx),
                                              self.canvas.canvasy(game.lasty))]])
        self.canvas.delete(self.selected)
        self.canvas.unbind("<Double-Button-1>")

    def do_dellink(self):
        if self.linkflag:
            game.action_q.append(['dellink',[self.link]])
            self.close()
            
    def do_addnode(self):
        if self.nodeflag:
            return
        else:
            self.msg_box_name('Enter a Network node name: ')
            self.close()
           

    def do_delnode(self):
        if self.nodeflag:
            game.action_q.append(['delnode',[self.node]])
            self.close()
        else:
            return

    # Display a message box for input
    def msg_box_name(self, msg, extra=True):
        top = self.top = Toplevel()
        top.resizable(FALSE,FALSE)
        label0 = Label(top, text=msg)
        label0.grid(column=0,row=0,columnspan=2,rowspan=2)

        if extra:
            self.entry0 = Entry(top)
            self.entry0.grid(column=0,row=2,rowspan=1,columnspan=3)

            button2 = Button(top, text='OK', command=self.submit_name)
            button2.grid(column=0,row=3,rowspan=1,columnspan=1)

        button3 = Button(top, text='Cancel',
                                command=lambda: self.top.destroy())
        button3.grid(column=2,row=3,rowspan=1,columnspan=1)

    def bindMouseRelease(self,shape,item):
        self.canvas.tag_bind(shape,"<ButtonPress-1>", lambda x: self.GetMaint(item))

    def submit_name(self):
        data = self.entry0.get()
        if data:
            self.name = data
            game.action_q.append((['addnode',[(self.x,self.y),self.name]]))
            self.top.destroy()
            self.close()




        
        
