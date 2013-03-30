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
    def __init__(self,x,y,canvas,node,network,imagedict,nodeflag=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.node = node
        self.network = network
        self.imagedict = imagedict
        
        # Define some fonts
        Font1 = font.Font(family='Arial', size=14, weight='bold')
        Font2 = font.Font(family='Helvetica', size=12, weight='bold')
        Font3 = font.Font(family='Arial', size=12)

        # The nodeflag tells whether or not a node was clicked on.
        self.nodeflag = nodeflag

        # Begin by drawing the submenu
        self.objects = []
        
        temp = canvas.create_rectangle(x,y,x + self.width,y + self.height,fill='white')
        self.objects.append(temp)


        
        
