import dict_reverselookup

from digraph import Digraph
import dyjkstra

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
        # A network graph will contain the game's main graph.
        # There will be an origin node whose coordinates are specified
        def __init__(self,origin_coord,origin_name,origin_items):
                self.graph = Digraph()
                self.vertex_counter = 1
                
                # This dictionary will contain the coordinates of
                # vertices in the graph
                self.V_coord = { }

                # This dictionary will contain the names of the vertices
                self.V_name = { }

                # These dictionaries will contain lists of  objects
                # located at specific vertices and edges
                self.V_items = { }
                self.E_items = { }

                # Add the info for the origin node
                self.graph.add_vertex(0)
                self.V_coord[0] = origin_coord
                self.V_name[0] = origin_name
                self.V_items[0] = origin_items

        # Creates a new network node. Takes a coordinate typle for the vertex,
        # a user specified name, and a list of items to be placed at the node. 
        # Can be an empty list. 
        def NewNode(self,coord,name,items):
                # Add the vertex to the graph
                # The vertex counter provisions ID's for each vertex
                self.graph.add_vertex(self.vertex_counter)

                # Add the coordinates of the node
                self.V_coord[self.vertex_counter] = coord

                self.V_name[self.vertex_counter] = name

                # Add the items to the vertex's inventory
                self.V_items[self.vertex_counter] = items
                
                # Increment vertex counter
                self.vertex_counter = self.vertex_counter + 1

        def AddEdge(self,st_node,end_node,items):
                # Add the edge to the graph. Note st_node and end_node are
                # the names of the nodes; not ID's
                
                e = (rev_lookup(self.V_name,st_node),rev_lookup(self.V_name,end_node))
                self.graph.add_edge(e)
                self.E_items[e] = items

        def AddItemsToNode(self,node_name,items):
                # Add items to a pre-existing node
                self.V_items[rev_lookup(self.V_name,node_name)].append(items)

        def AddItemsToEdge(self,st_node,end_node,items):
                # Add items to a pre-existing edge
                e = (rev_lookup(self.V_name,st_node),rev_lookup(self.V_name,end_node))
                self.E_items[e].append(items)

if __name__ == "__main__":
        import doctest
        doctest.testmod()
