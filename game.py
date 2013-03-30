import random
import math
from tkinter import messagebox
from agentsim import GUI

# Import network graph
from networkgraph import *
from database import *
from capital import *
from nodedisplay import *
from canvassubmenu import *

import LEVEL1_map

# Globals for mouse clicks.
global lastx, lasty
global mode

# Event callbacks:
def xy(event):
        global lastx, lasty
        lastx = event.x
        lasty = event.y

class Game:
        def __init__(self,title="Telecom Simulation"):

                # Load up teh item database
                self.ItemDatabase = CapitalDatabase()

                # Initialize message stack. 
                # This stack will contain the messages 
                # which will display at turns.
                self._messages = []
                
                
                # let us modify the value of the global gui variable
                global gui
                gui = GUI(init_fn=self.do_init, step_fn=self.do_turn, xmax=1200,ymax=1400,title=title)

        def start(self):
                gui.start()

        def do_init(self):
                self.gameNetwork = NetworkGraph((500,500),"Station Square",[],100000)

                LEVEL1_map.level1_setup(self)

                # Initialize message stack
                self._messages = []

                # Initialize game parameters:
                self.cash = 10000000
                self.turn = 1

                # Load images
                self.loadImages()

                self.subwindows = []
                global mode
                mode = 0

                # Load up the canvas, load up bg
                self._canvas = gui.get_canvas()       
                self.bg_image = self._canvas.create_image(0,0,image=self.icons['bg'],anchor='nw')

                # Bind text
                self.cashLabel = gui.get_cashlabel()
                self.cashcontents = StringVar()
                self.cashLabel['textvariable'] = self.cashcontents
                self.cashcontents.set(' $ ' + str(self.cash))

                # Bind mouse motion
                self._canvas.bind("<ButtonPress-1>", xy)
                self._canvas.bind("<ButtonPress-2>", xy)

                # Initialize a dictionary of lines objects
                self.E_lines = { }
                self.E_direction_marker = { }

                for edge in self.gameNetwork.GetEdges():
                        self.NewEdgeCanvas(edge)
                        
                # Initialize dictionary of node imagery
                self.V_images = { }
                self.V_notify = { }
                self.V_displays = set()
                self.V_text = { }
                for node in self.gameNetwork.GetNodes():
                        self.NewNodeCanvas(node)

        # Function adds new edge imagery dicitonaries and canvas
        def NewEdgeCanvas(self,edge):
                (x1,y1) = self.gameNetwork.V_coord[edge[0]]
                (x2,y2) = self.gameNetwork.V_coord[edge[1]]

                # Color code nodes by operation
                if len(self.gameNetwork.E_items[edge]) > 0:
                        fillcolor = 'green'
                else:
                        fillcolor='black'

                self.E_lines[edge] = self._canvas.create_line(x1,y1,x2,y2,fill=fillcolor,activefill='purple',width=3)
                (mid_x,mid_y) = midpoint((x1,y1),(x2,y2))

                # Draw indicator for bidirectional links
                (mid2_x,mid2_y) = midpoint((mid_x,mid_y),(x2,y2))
                self.E_direction_marker[edge] = self._canvas.create_line(mid2_x,mid2_y,
                                                                         mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) + 3 * math.pi/4),
                                                                         mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) + 3 * math.pi/4),
                                                                         fill='blue',width=2)
                self.E_direction_marker[edge] = self._canvas.create_line(mid2_x,mid2_y,
                                                                         mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) - 3 * math.pi/4),
                                                                         mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) - 3 * math.pi/4),
                                                                         fill='blue',width=2)
        # Function adds new node imagery dictionaries and canvas
        def NewNodeCanvas(self,node):
                (x,y) = self.gameNetwork.V_coord[node]
                self.V_images[node] = self._canvas.create_image(x,y,
                                                                image=self.icons['tower1'],
                                                                activeimage=self.icons['tower1_active'],
                                                                anchor='center')
                self.V_text[node] = self._canvas.create_text(x + 10,y,
                                                             text=(self.gameNetwork.V_name[node] + '\n' + self.gameNetwork.ItemsAtNode(node) + ' items'),
                                                             anchor='w',fill='white')
                # Attach mouse events to each node iamge
                self._canvas.tag_bind(self.V_images[node],"<ButtonRelease-1>", lambda x: self.displayNode(node))
                self._canvas.tag_bind(self.V_images[node],"<ButtonRelease-2>", lambda x: self.submenuNode(node))

        # Creates an instance of a window to display the node data.
        def displayNode(self,node):
                self.V_displays.add(node)
                self.subwindows.append(NodeDisplay(self._canvas.canvasx(lastx),
                                                   self._canvas.canvasy(lasty),
                                                   self._canvas,node,self.gameNetwork,
                                                   self.icons,gui.GetRoot()))

        # Display a right-click submenu on the canvas
        def submenuNode(self,node):
                menu = CanvasSubMenu(self._canvas.canvasx(lastx),
                                     self._canvas.canvasy(lasty),
                                     self._canvas,node,self.gameNetwork,
                                     self.icons,nodeflag=1)
                
        # Loads a dictionary of imags
        def loadImages(self):
                self.icons = { }
                self.icons['tower1'] = PhotoImage(file = 'images/tower.gif')
                self.icons['tower1_active'] = PhotoImage(file = 'images/tower_active.gif')
                self.icons['bg'] = PhotoImage(file = 'images/terrain.gif')
                self.icons['close']= PhotoImage(file = 'images/close.gif')
                self.icons['close_active']= PhotoImage(file = 'images/close_active.gif')
                self.icons['addbutton']= PhotoImage(file = 'images/addbutton.gif')
                self.icons['addbutton_active']= PhotoImage(file = 'images/addbutton_active.gif')
                self.icons['notify']= PhotoImage(file = 'images/notify.gif')

        def do_turn(self):
                total_maintCost = 0
                # Refresh ll stat windows, which will be inaccurate
                for window in self.subwindows:
                        if not window.Closed():
                                window.refresh()
                        else:
                                self.subwindows.remove(window)

                # Updat all of the items at nides for a turn.
                for nodeKey in self.gameNetwork.V_items.keys():
                        for item in self.gameNetwork.V_items[nodeKey]:
                                fail = item.Update()
                                # Add a message telling what failed and where, if it did.
                                if fail == True:
                                        self._messages.append(item.GetName() + " failed at " + self.gameNetwork.V_name[nodeKey])
                                        self.V_notify[nodeKey ] = self._canvas.create_image(self.gameNetwork.V_coord[nodeKey][0] - 8,
                                                                                           self.gameNetwork.V_coord[nodeKey ][1] - 16,
                                                                                           image=self.icons['notify'],
                                                                                           anchor='se')
                                                                  
                                else:
                                        # Record maintennace cost
                                        total_maintCost = total_maintCost + item.GetMaintenance()
                                        
                # Update items at edges
                for edgekey in self.gameNetwork.E_items.keys():
                        for item in self.gameNetwork.E_items[edgekey]:
                                fail = item.Update()
                                # Add a message telling what failed and where, if it did.
                                if fail == True:
                                        self._messages.append(item.GetName() + " failed ")
                                        self._canvas.itemconfigure(self.E_lines[edgekey],fill='red')
                                else:
                                        # Record maintennace cost
                                        total_maintCost = total_maintCost + item.GetMaintenance()
                                
                
                # Update how much money to make:
                revenue = 0

                # Needs to be implemented here.....


                # Update game parameters
                self.cash = self.cash - total_maintCost + revenue
                self.turn = self.turn + 1

                self.cashcontents.set(' $ ' + str(self.cash))
                
                # Empty the message stack to the user.
                while len(self._messages) > 0:
                        messagebox.showinfo("Message",self._messages.pop(0),
                                            icon='warning')

def rgb_to_color(r, g, b):
    """
		Utility to generate a Tk color rgb string from  integer r, g, b,
		where 0 <= r, g, b <= 1
		
		Use as in
        agentsim.gui.get_canvas().create_oval(10, 20, 30, 40,
		fill=agentsim.rgb_to_color(.8, .8, 0) )
		"""
	
    return '#{0:02x}{1:02x}{2:02x}'.format(
										   int((r * 255) % 256), int((g * 255) % 256), int((b * 255) % 256), )

def midpoint(pt1,pt2):
        (x1,y1) = pt1
        (x2,y2) = pt2
        return ((x1+x2)//2,(y1+y2)//2)


