import random
import math
from agentsim import GUI

# Import network graph
from networkgraph import NetworkGraph

from database import CapitalDatabase

class Game:
        def __init__(self,init_fn=None, step_fn=None, title="Simulation"):

                ItemDatabase = CapitalDatabase()
                GameNetwork = NetworkGraph((0,0),"Edmonton",[],100000)
                # let us modify the value of the global gui variable
                global gui
                gui = GUI(init_fn=init_fn, step_fn=step_fn, title=title)
        def start(self):
                gui.start()

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
