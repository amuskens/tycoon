from digraph import Digraph

from capital import Item
from capital import Structure
from capital import Building
from capital import Tower
from capital import Network
from capital import Router
from capital import PointToPoint
from capital import Radio
from capital import Wired

class NetworkGraph:
	# A network graph will contain the game's main graph
	def __init__(self):
		self.graph = Digraph()




if __name__ == "__main__":
    import doctest
    doctest.testmod()