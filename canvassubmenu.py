# Defines a submenu for the canvas accessed by right click

from tkinter import *
import copy

from game import *
from capital import *
from database import *
from networkgraph import *
from subslotedit import *
from getvaluedialog import *

class CanvasSubMenu():
    def __init__(self,x,y,canvas,nodeorlink,network,imagedict,nodeflag=0,linkflag=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.network = network
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
        if nodeflag:
            image1 = self.imagedict['addlink']
            image2 = self.imagedict['addlink_active']
            image3 = self.imagedict['dellink']
            image4 = self.imagedict['dellink_active']
            image5 = self.imagedict['addnode_inactive']
            image6 = self.imagedict['addnode_inactive']
            image7 = self.imagedict['delnode']
            image8 = self.imagedict['delnode_active']
        elif linkflag:
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

        self.addlink = canvas.create_image(x + 200,y,
                                           image=image1,
                                           activeimage=image2,
                                           anchor='nw')
        
        self.dellink = canvas.create_image(x + 300,y,
                                           image=image3,
                                           activeimage=image4,
                                           anchor='nw')

        self.addnode = canvas.create_image(x,y,
                                           image=image5,
                                           activeimage=image6,
                                           anchor='nw')
        self.delnode = canvas.create_image(x + 100,y,
                                           image=image7,
                                           activeimage=image8,
                                           anchor='nw')



        
        
