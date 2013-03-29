import random
import math
from agentsim import GUI

# Import network graph
from networkgraph import *
from database import *
from capital import *

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
                self.gameNetwork = NetworkGraph((500,500),"Edmonton",[],100000)

                # Test network, showing a demo of how to use the functions:
                self.gameNetwork.NewNode((480,800),"Calgary",[])
                self.gameNetwork.AddEdge("Edmonton","Calgary",[])
                self.gameNetwork.NewNode((300,810),"Banff",[])
                self.gameNetwork.AddEdge("Banff","Calgary",[])
                self.gameNetwork.NewNode((600,200),"Fort McMurray",[])
                self.gameNetwork.AddEdge("Edmonton","Fort McMurray",[])
                self.gameNetwork.AddItemsToNode("Edmonton",[self.ItemDatabase.GetRadio(0),self.ItemDatabase.GetRadio(1)])

                # Initialize message stack
                self._messages = []
                self._messages.append("Welcome to Telecom Netowrk Tycoon!")

                # Initialize game parameters:
                self.cash = 10000000
                self.turn = 1

                # Load images
                self.loadImages()

                # Load up the canvas
                self._canvas = gui.get_canvas()       

                # Bind text
                self.cashLabel = gui.get_cashlabel()
                self.cashcontents = StringVar()
                self.cashLabel['textvariable'] = self.cashcontents
                self.cashcontents.set(' $ ' + str(self.cash))

                # Initialize a dictionary of lines
                self.E_lines = { }
                for edge in self.gameNetwork.GetEdges():
                        (x1,y1) = self.gameNetwork.V_coord[edge[0]]
                        (x2,y2) = self.gameNetwork.V_coord[edge[1]]
                        self.E_lines[edge] = self._canvas.create_line(x1,y1,x2,y2,fill='green',width=3)
                
                # Initialize dictionary of node imagery
                self.V_images = { }
                self.V_text = { }
                for node in self.gameNetwork.GetNodes():
                        (x,y) = self.gameNetwork.V_coord[node]
                        self.V_images[node] = self._canvas.create_image(x,y,image=self.icons['tower1'],anchor='center')
                        self.V_text[node] = self._canvas.create_text(x + 10,y,
                                                                     text=(self.gameNetwork.V_name[node] + '\n' + self.gameNetwork.ItemsAtNode(node) + ' items'),
                                                                     anchor='w')

        # Loads a dictionary of imags
        def loadImages(self):
                self.icons = { }
                self.icons['tower1'] = PhotoImage(file = 'images/tower.gif')

        def do_turn(self):
                total_maintCost = 0
                # Updat all of the items at nides for a turn.
                for nodeKey in self.gameNetwork.V_items.keys():
                        for item in self.gameNetwork.V_items[nodeKey]:
                                fail = item.Update()
                                # Add a message telling what failed and where, if it did.
                                if fail == True:
                                        self._messages.append(item.GetName() + " failed at " + self.gameNetwork.V_names[nodeKey])
                                else:
                                        # Record maintennace cost
                                        total_maintCost = total_maintCost + item.GetMaintenance()
                                        
                                
                                
                # Update game parameters
                self.cash = self.cash - total_maintCost
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
