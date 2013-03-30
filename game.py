import random
import math
from agentsim import GUI

# Import network graph
from networkgraph import *
from database import *
from capital import *

import LEVEL1_map

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

                # Test network, showing a demo of how to use the functions:
                """
                self.gameNetwork.NewNode((480,800),"Anders City",[self.ItemDatabase.GetTower(1)])
                self.gameNetwork.AddEdge("Station Square","Anders City",[self.ItemDatabase.GetRadio(3)])
                self.gameNetwork.AddEdge("Anders City","Station Square",[self.ItemDatabase.GetRadio(3)])
                self.gameNetwork.NewNode((300,810),"IslandVille",[])
                self.gameNetwork.AddEdge("IslandVille","Anders City",[])
                self.gameNetwork.NewNode((800,50),"Oil City",[])
                self.gameNetwork.AddEdge("Station Square","Oil City",[])
                self.gameNetwork.AddEdge("Oil City","Station Square",[self.ItemDatabase.GetRadio(0)])
                self.gameNetwork.AddItemsToNode("Station Square",[self.ItemDatabase.GetTower(0),self.ItemDatabase.GetTower(1)])
                """

                LEVEL1_map.level1_setup(self)


                # Initialize message stack
                self._messages = []
                self._messages.append("Welcome to Telecom Netowrk Tycoon!")

                # Initialize game parameters:
                self.cash = 10000000
                self.turn = 1

                # Load images
                self.loadImages()

                # Load up the canvas, load up bg
                self._canvas = gui.get_canvas()       
                self.bg_image = self._canvas.create_image(0,0,image=self.icons['bg'],anchor='nw')

                # Bind text
                self.cashLabel = gui.get_cashlabel()
                self.cashcontents = StringVar()
                self.cashLabel['textvariable'] = self.cashcontents
                self.cashcontents.set(' $ ' + str(self.cash))

                # Initialize a dictionary of lines objects
                self.E_lines = { }
                self.E_direction_marker = { }

                for edge in self.gameNetwork.GetEdges():
                        self.NewEdgeCanvas(edge)
                        
                # Initialize dictionary of node imagery
                self.V_images = { }
                self.V_text = { }
                for node in self.gameNetwork.GetNodes():
                        self.NewNodeCanvas(node)

        # Function adds new edge imagery dicitonaries and canvas
        def NewEdgeCanvas(self,edge):
                (x1,y1) = self.gameNetwork.V_coord[edge[0]]
                (x2,y2) = self.gameNetwork.V_coord[edge[1]]

                self.E_lines[edge] = self._canvas.create_line(x1,y1,x2,y2,fill='green',width=3)
                (mid_x,mid_y) = midpoint((x1,y1),(x2,y2))

                # Draw indicator for bidirectional links
                (mid2_x,mid2_y) = midpoint((mid_x,mid_y),(x2,y2))
                self.E_direction_marker[edge] = self._canvas.create_line(mid2_x,mid2_y,
                                                                         mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) + 3 * math.pi/4),
                                                                         mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) + 3 * math.pi/4),
                                                                         fill='green',width=2)
                self.E_direction_marker[edge] = self._canvas.create_line(mid2_x,mid2_y,
                                                                         mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) - 3 * math.pi/4),
                                                                         mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) - 3 * math.pi/4),
                                                                         fill='green',width=2)
        # Function adds new node imagery dictionaries and canvas
        def NewNodeCanvas(self,node):
                (x,y) = self.gameNetwork.V_coord[node]
                self.V_images[node] = self._canvas.create_image(x,y,image=self.icons['tower1'],anchor='center')
                self.V_text[node] = self._canvas.create_text(x + 10,y,
                                                             text=(self.gameNetwork.V_name[node] + '\n' + self.gameNetwork.ItemsAtNode(node) + ' items'),
                                                             anchor='w',fill='white')

        # Loads a dictionary of imags
        def loadImages(self):
                self.icons = { }
                self.icons['tower1'] = PhotoImage(file = 'images/tower.gif')
                self.icons['bg'] = PhotoImage(file = 'images/terrain.gif')

        def do_turn(self):
                total_maintCost = 0
                # Updat all of the items at nides for a turn.
                for nodeKey in self.gameNetwork.V_items.keys():
                        for item in self.gameNetwork.V_items[nodeKey]:
                                fail = item.Update()
                                # Add a message telling what failed and where, if it did.
                                if fail == True:
                                        self._messages.append(item.GetName() + " failed at " + self.gameNetwork.V_name[nodeKey])
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

                print(self.cash)
                print(self._messages)


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
