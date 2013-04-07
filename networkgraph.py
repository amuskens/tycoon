import dict_functions
from distfuncs import *

from digraph import Digraph
import dyjkstra

from capital import *

class NetworkGraph:
	# A network graph will contain the game's main graph.
	# There will be an origin node whose coordinates are specified
	def __init__(self,origin_coord,origin_name,origin_items,origin_startbandwidth):
		self.graph = Digraph()
		self.vertex_counter = 1
		self.max_slots = 3
		self.scale_factor = 1 / 4
		
		# This dictionary will contain the coordinates of
		# vertices in the graph
		self.V_coord = { }

		# This dictionary will contain the names of the vertices
		self.V_name = { }

		# These dictionaries will contain lists of  objects
		# located at specific vertices and edges
		self.V_items = { }
		self.E_items = { }

		# Figure out the link distances beforehand, and cache them
		self.E_lengths = { }

		# Add the info for the origin node
		self.graph.add_vertex(0)
		self.V_coord[0] = origin_coord
		self.V_name[0] = origin_name
		self.V_items[0] = origin_items

		# Set the start bandwidth at the origin
		self.origin_bandwidth = origin_startbandwidth

	# Returns max slots
	def GetMaxSlots(self):
		return self.max_slots

	# Returns the set of edges in the graph
	def GetEdges(self):
		return self.graph.edges()

	# Returns the set of vertices in the graph
	def GetNodes(self):
		return self.graph.vertices()

	# Get the node number from the node name
	def GetNodeNumber(self,node_name):
		return rev_lookup(self.V_name,node_name)

	# Returns a list of items at the node
	def NodeGetItems(self,node_name):
		return self.V_items[rev_lookup(self.V_name,node_name)]
		
	# Returns a list of items at the edge from st_node name to end_node name
	def EdgeGetItems(self,st_node,end_node):
		e = (rev_lookup(self.V_name,st_node),rev_lookup(self.V_name,end_node))
		return self.E_items[e]

	# Get the coordinates of a node
	def GetNodeCoord(self,node_name):
		return self.V_name[rev_lookup(self.V_name,node_name)]

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
		
		node = self.vertex_counter

		# Increment vertex counter
		self.vertex_counter = self.vertex_counter + 1

		# Return the node ID
		return node

		

	# Get the number of items at the node
	def ItemsAtNode(self,node_num):
		return str(len(self.V_items[node_num]))

	# Add an edge by ID
	def AddEdgeID(self,st_node,end_node,items):
		e = (st_node,end_node)
		self.graph.add_edge(e)
		self.E_items[e] = items
		(x1 ,y1) = self.V_coord[e[0]]
		(x2, y2) = self.V_coord[e[1]]
		self.E_lengths[e] = dist(x1 ,y1, x2, y2) * self.scale_factor

	# Add the edge to the graph. Note st_node and end_node are
	# the names of the nodes; not ID's
	def AddEdge(self,st_node,end_node,items):
		e = (rev_lookup(self.V_name,st_node),rev_lookup(self.V_name,end_node))
		self.AddEdgeID(e[0],e[1],items)

	# Add items to a pre-existing node
	def AddItemsToNode(self,node_name,items):
		for item in items:
			if len(self.V_items[rev_lookup(self.V_name,node_name)]) <= self.max_slots:
				self.V_items[rev_lookup(self.V_name,node_name)].append(item)
	

	# Add items to a pre-existing edge. Note these should only be point to point type items.
	def AddItemToEdge(self,edge,item):
		if item.type() == 'Radio':
			# Deal with the start. Find the first non full tower.
			# We need to make sure there is a tower available at the
			# start and end node
			st_tower = None
			for itema in self.V_items[edge[0]]:
				if itema.MaxLinks():
					continue
				elif itema.StructType() == 'Tower':
					st_tower = itema
					break
			en_tower = None
			for itema in self.V_items[edge[1]]:
				print(itema)
				if itema.MaxLinks():
					continue
				elif itema.StructType() == 'Tower':
					en_tower = itema
					break

			if st_tower and en_tower:
				# We're good. A position is available,
				# since a link slot is available at both
				# the start and end
				st_tower.AddLink()
				en_tower.AddLink()
				self.E_items[edge].append(item)
				return True
			else:
				return False

		elif item.type() == 'Wired':
			# Same idea
			st_build = None
			for itema in self.V_items[edge[0]]:
				if itema.MaxLinks():
					continue
				elif itema.StructType() == 'Building':
					st_build = itema
					break
			en_build = None
			for itema in self.V_items[edge[1]]:
				if itema.MaxLinks():
					continue
				elif itema.StructType() == 'Building':
					en_build = itema
					break

			if st_build and en_build:
				# We're good. A position is available,
				# since a link slot is available at both
				# the start and end
				st_build.AddLink()
				en_build.AddLink()
				self.E_items[edge].append(item)
				return True
			else:
				return False
		return False

	# Removes items in the list from a node
	def RemoveItemsFromNode(self,node_name,items):
		for i in items:
			if i in self.V_items[rev_lookup(self.V_name,node_name)]:
				self.V_items[rev_lookup(self.V_name,node_name)].remove(i)

	# Removes items in the list from a node
	def RemoveItemFromEdge(self,edge,index):
		if self.E_items[edge][index] == 'Radio':
			# FInd first start and end towers
			# Make sure we find one that has links
			st_tower = None
			for item in self.V_items[edge[0]]:
				if item.StructType() == 'Tower' and not item.NoLinks():
					st_tower = item
					break
			en_tower = None
			for item in self.V_items[edge[1]] and not item.NoLinks():
				if item.StructType() == 'Tower':
					en_tower = item
					break

			if st_tower and en_tower:
				# We found the towers. Now we can remove the item.
				st_tower.RemoveLink()
				en_tower.RemoveLink()
				return self.V_items[edge].pop(index)
			return None

		elif self.E_items[edge][index] == 'Wired':
			# FInd first start and end towers
			# Make sure we find one that has links
			st = None
			for item in self.V_items[edge[0]]:
				if item.StructType() == 'Building' and not item.NoLinks():
					st = item
					break
			en = None
			for item in self.V_items[edge[1]] and not item.NoLinks():
				if item.StructType() == 'Building':
					en = item
					break

			if st and en:
				# We found the towers. Now we can remove the item.
				st.RemoveLink()
				en.RemoveLink()
				return self.V_items[edge].pop(index)
			return None
		return None


	# Determine an edge's operational status
	def EdgeOperational(self,e):
		for item in self.E_items[e]:
			if not item.Operating(): return False
		return True

	# Determine a node's operational status
	def NodeOperational(self,node_num):
		for item in self.V_items[node_num]:
			if not item.Operating(): return False
			if item.type() == 'Structure':
				for subitem in item.GetInventory():
					if not subitem.Operating(): return False
		return True

	# Return the number of link slots at a node
	def NodeLinkSlots(self,node):
		radio_linkslots = 0
		wired_linkslots = 0
		maxradio_linkslots = 0
		maxwired_linkslots = 0
		for item in self.V_items[node]:
			if item.StructType() == 'Tower':
				radio_linkslots = radio_linkslots +  item.GetCurLinkSlots()
				maxradio_linkslots = maxradio_linkslots +  item.GetMaxLinkSlots()

			elif item.StructType() == 'Building':
				wired_linkslots = wired_linkslots +  item.GetCurLinkSlots()
				maxwired_linkslots = maxwired_linkslots +  item.GetMaxLinkSlots()

		return (radio_linkslots,
			wired_linkslots,
			maxradio_linkslots,
			maxwired_linkslots)
				
	# Temp Cost function
	def cost(self,e):
		return 1

	# Max capacity available at an edge
	def MaxCapAtEdge(self,edge):
		cap = 0
		for item in self.E_items[edge]:
			cap = cap + item.GetMaxCapacity()

		return cap

	# Calculate the bandwidth available at a node
	def BandwidthAtNode(self,node_name):
		node = rev_lookup(self.V_name,node_name)
		path = least_cost_path(self.graph,0,node,self.cost)
		if path == None: return 0
		# Calculate.... NOt done yet   

	# Returns the node closest to the point
	def ReturnClosePoint(self,pt):
		(x,y) = pt
		dist_array = []
		for ids in self.V_items.keys():
			# Populate a list of distances to the start point
			dist_array.append((ids,
					   dist(x,
						y,
						self.V_coord[ids][0],
						self.V_coord[ids][1])))
		# The smallest element is closest
		(id,dist1) = min(dist_array, key=lambda x: x[1])
		return (id,dist1)


def rev_lookup(dict,item):
	"""
	Tests:	
	>>> a = { }
	>>> a['Hi'] = 5
	>>> a[56] = 234
	>>> rev_lookup(a,5)
	'Hi'
	>>> rev_lookup(a,234)
	56
	"""
	for key in dict.keys():
		if dict[key] == item:
			return key

	return None

if __name__ == "__main__":
	import doctest
	doctest.testmod()
