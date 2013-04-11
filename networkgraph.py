import dict_functions
from distfuncs import *

from digraph import Digraph
import dyjkstra
import math

from capital import *

class NetworkGraph:
	# A network graph will contain the game's main graph.
	# There will be an origin node whose coordinates are specified
	def __init__(self,scale_factor = 0.2):
		self.graph = Digraph()
		self.vertex_counter = 1
		self.max_slots = 3
		self.scale_factor = scale_factor
		
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

		# These are used for calculating capacity at nodes and edges
		self.cap_at_node = {}
		self.cap_at_edge = {}
		self.cap_at_node_cached = {}
		self.cap_at_edge_cached = {}

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

	# Delete a network node
	def DelNode(self,node):
		items_at_node = []

		if node in self.graph.vertices():
			self.graph.del_vertex(node)
			items_at_node = self.V_items[node]
		
			# Delete the node from dictionaries
		
			del self.V_items[node]
			del self.V_coord[node]
			del self.V_name[node]

		return items_at_node

	# Delete a network link
	def DelLink(self,edge):
		items_at_edge = []

		if edge in self.graph.edges():
			self.graph.del_edge(edge)
			items_at_edge = self.E_items[edge]

			# Delete
			del self.E_items[edge]
			del self.E_lengths[edge]
		
		return items_at_edge

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
		item = self.E_items[edge][index]
		if item.type() == 'Radio':
			# Deal with the start. Find the first non full tower.
			# We need to make sure there is a tower available at the
			# start and end node
			st_tower = None
			for itema in self.V_items[edge[0]]:
				if itema.NoLinks():
					continue
				elif itema.StructType() == 'Tower':
					st_tower = itema
					break
			en_tower = None
			for itema in self.V_items[edge[1]]:
				if itema.NoLinks():
					continue
				elif itema.StructType() == 'Tower':
					en_tower = itema
					break

			if st_tower and en_tower:
				# We're good. A position is available,
				# since a link slot is available at both
				# the start and end
				st_tower.RemoveLink()
				en_tower.RemoveLink()
				self.E_items[edge].pop(index)
				return True
			else:
				return False

		elif item.type() == 'Wired':
			# Same idea
			st_build = None
			for itema in self.V_items[edge[0]]:
				if itema.NoLinks():
					continue
				elif itema.StructType() == 'Building':
					st_build = itema
					break
			en_build = None
			for itema in self.V_items[edge[1]]:
				if itema.NoLinks():
					continue
				elif itema.StructType() == 'Building':
					en_build = itema
					break

			if st_build and en_build:
				# We're good. A position is available,
				# since a link slot is available at both
				# the start and end
				st_build.RemoveLink()
				en_build.RemoveLink()
				self.E_items[edge].pop(index)
				return True
			else:
				return False
		return False		


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

		# Check each item at the node
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
				
	# Cost is determined by the greatest available capacity at a link
	# Cost is inversely proportional to the available capacity
	# This function will be used by Dyjkstra's algorithm to route data in the 
	# most efficient way possible, avoiding bottlenecks and links with 
	# too little capacity. This way, links with the greatest capacity will fill up first.
	def cost(self,e):
		cost = self.cap_at_edge[e]

		# Avoid that nasty divide by zero error.
		if cost == 0: return 0

		return 1/cost
		

	# Max capacity at a node
	def MaxCapAtNode(self,node):
		cap = 0
		connections = len(self.graph.adj_to(node))
		for item in self.V_items[node]:
			for subitem in item.GetInventory():
				cap = cap + subitem.GetMaxCapacity()

				# Give a bonus for different router types
				if subitem.type() == 'Router':
					if subitem.RouterType() == 'Multiplexer':
						cap = cap + (subitem.GetMaxCapacity()) * 10 * connections / (math.log10(connections) + 0.0000000001)
		return cap

	# Max capacity available at an edge
	def MaxCapAtEdge(self,edge):
		cap = 0
		for item in self.E_items[edge]:
			cap = cap + item.GetMaxCapacity()

		return cap

	# Returns the traffic engineered capacity at the edge
	def CapAtEdge(self,edge):
		cap = 0
		for item in self.E_items[edge]:
			cap = cap + item.GetCapacity()

		return cap

	# Returns the node closest to the point
	def ReturnClosePoint(self,pt):
		(x,y) = pt
		dist_array = []
		for ids in self.V_items.keys():
			# Populate a list of distances to the start point
			dist_array.append((ids,
					   dist(x,y,
						self.V_coord[ids][0],
						self.V_coord[ids][1])))
		# The smallest element is closest
		(id,dist1) = min(dist_array, key=lambda x: x[1])
		return (id,dist1)

	# Returns a close point within the threshhold
	def ReturnClosePointThresh(self,pt,thresh):
		(x,y) = pt
		dist_array = []
		for ids in self.V_items.keys():
			# Populate a list of distances to the start point
			distance = dist(x,y,self.V_coord[ids][0],self.V_coord[ids][1])
			if distance < thresh:
				dist_array.append((ids,distance))

		# The smallest element is closest
		if dist_array:
			(id,dist1) = min(dist_array, key=lambda x: x[1])
			return (id,dist1)
		else:
			return None

	# Resets the cap at node and cap at edge dictioanries
	def CapReset(self):
		del self.cap_at_node
		del self.cap_at_edge
		self.cap_at_node = {}
		self.cap_at_edge = {}
		# Compile base capacities
		for n in self.graph.vertices():
			self.cap_at_node[n] = self.MaxCapAtNode(n)

		for e in self.graph.edges():
			self.cap_at_edge[e] = self.MaxCapAtEdge(e)

	# Save the capacities so we can recover them for display
	def CapCache(self):
		self.cap_at_node_cached = copy.deepcopy(self.cap_at_node)
		self.cap_at_edge_cached = copy.deepcopy(self.cap_at_node)

	# Calculate the bandwidth available at a certain coordinate point.
	# This function will be used to calculate revenue
	# Premise is to use Dyjkstra's algorithm from every node near a city to every other node near every other city.
	# While doing so, we will add up the current traffic flows through links and nodes in order to figure out
	# how saturated links are, and restrict traffic flow accordingly.
	def CapAtCoord(self,pt,to_pts):
		(x, y) = pt

		# Make a list of nodes which are within 100 units of the point.
		closest = []
		for ids in self.V_items.keys():
			# Populate a list of distances to the start point
			distance = dist(x,y,self.V_coord[ids][0],self.V_coord[ids][1])
			if distance < 200: 
					closest.append(ids)

		# Find the nodes nearest to other cities
		to_nodes = []
		for pts in to_pts:
			if pts == pt: continue
			n = self.ReturnClosePointThresh(pts,100)
			if n:
				to_nodes.append(n[0])

		# we now can calculate the available bandwidth from every city to every other city

		# Now step over the list and find paths for the outgoing supply
		total_outgoing_supply = 0
		for node in closest:
			for to_node in to_nodes:
				if to_node == node: continue
				
				# Find the path to the other node
				path = dyjkstra.least_cost_path(self.graph,node,to_node,self.cost)
				if not path:
					continue
				
				# Step through the path and see how much bandwidth is available
				index = 0
				
				#print('Outgoing start:')

				# If the edge does not have enough caacity, cap flow at this amount
				cur_cap = self.cap_at_edge[(path[0],path[1])]
				#print(cur_cap)
				while index < len(path) - 1 and cur_cap > 0:
					# Step through and calculate bandwidth
					
					# If we got through a router at a node, it will
					# cap the capacity at its max.
					if cur_cap >= self.cap_at_node[path[index]]:
						cur_cap = self.cap_at_node[path[index]]
						
					# Subtract the target capacity
					self.cap_at_node[index] = sub_azero(self.cap_at_node[path[index]],cur_cap)
					
					# Send capacity over a link and cap it at the max
					if cur_cap >= self.cap_at_edge[(path[index],path[index + 1])]:
						cur_cap = self.cap_at_edge[(path[index],path[index + 1])]

					# Subtract the target capacity from the edge
					self.cap_at_edge[(index,index + 1)] = sub_azero(self.cap_at_edge[(path[index],path[index + 1])],cur_cap)

					index = index + 1

				total_outgoing_supply = total_outgoing_supply + cur_cap

		# Do the same thing for incoming supply
		total_incoming_supply = 0
		for node in to_nodes:
			for to_node in closest:
				if to_node == node: continue
				
				# Find the path to the other node
				path = dyjkstra.least_cost_path(self.graph,node,to_node,self.cost)
				if not path:
					continue
				
				# Step through the path and see how much bandwidth is available
				index = 0
				#print('Incoming start:')
				
				cur_cap = self.cap_at_edge[(path[0],path[1])]
				#print(cur_cap)
				while index < len(path) - 1 and cur_cap > 0:
					# Step through and calculate bandwidth
					
					# If we got through a router at a node, it will
					# cap the capacity at its max.
					if cur_cap >= self.cap_at_node[path[index]]:
						cur_cap = self.cap_at_node[path[index]]
						
					# Subtract the target capacity
					self.cap_at_node[index] = sub_azero(self.cap_at_node[path[index]],cur_cap)
					
					# Send capacity over a link and cap it at the max
					if cur_cap >= self.cap_at_edge[(path[index],path[index+1])]:
						cur_cap = self.cap_at_edge[(path[index],path[index+1])]

					# Subtract the target capacity from the edge
					self.cap_at_edge[(index,index + 1)] = sub_azero(self.cap_at_edge[(path[index],path[index+1])],cur_cap)

					index = index + 1

				total_incoming_supply = total_incoming_supply + cur_cap
		
		# Return the values
		#print(str(total_outgoing_supply) + ' ' + str(total_incoming_supply))
		return (total_outgoing_supply,total_incoming_supply)
		
				
		
# Look up an item backwards in a dictionary
# Assumes that every item is unique even across multiple keys.
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

# Subtraction, but not below zero. Cap at 0
def sub_azero(a,b):
	if a < 0: 
		a = 0
	c = a - b
	if c < 0:
		c = 0
	return c


if __name__ == "__main__":
	import doctest
	doctest.testmod()
