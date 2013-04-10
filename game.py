# game.py
# Contians the main game class, which holds all other game classes inside.

import random
import math
import copy
from tkinter import messagebox
from agentsim import GUI

# Import network graph
from networkgraph import *
from database import *
from capital import *
from nodedisplay import *
from canvassubmenu import *
from economic import *
from city import *
from editlink import *
from distfuncs import *
import store
import editnode

import LEVEL1_map

# Globals for mouse clicks.
global lastx, lasty
global mode
global RightCounter
global action_q
action_q = []

"""

There will be use of a global "action queu" which other
class can use to send actions to the game class. This will be popped
until emptied every step, and the instruction swill be executed.

Action format:
[ <action string>, [ <action argument list. ] ]

"""

	


# Event callbacks:
def xy(event):
	global lastx, lasty, clicked
	lastx = event.x
	lasty = event.y
	clicked = True

class Game:
	def __init__(self,title="Telecom Network Tycoon"):

		# Load up teh item database
		self.ItemDatabase = CapitalDatabase()

		# Initialize message stack. 
		# This stack will contain the messages 
		# which will display at turns.
		self._messages = []
		self.inventory = []
		self.cash = 500000
		
		# let us modify the value of the global gui variable
		global gui
		gui = GUI(copy.copy(self.inventory),self.ItemDatabase,
			  init_fn=self.do_init, step_fn=self.do_turn, 
			  xmax=2600,ymax=2400,title=title)

	def start(self):
		gui.start()

	def do_init(self):
		global lastx, lasty
		global RightCounter
		RightCounter=1
		self.gameNetwork = NetworkGraph((800,800),"Root",[],100000)

		self.economy = LEVEL1_map.level1_setup(self)
		
		# Initialize message stack
		self._messages = []

		# Initialize the action queue
		global action_q
		action_q = []

		# Initialize game parameters:
		self.inventory = []
		self.loans = []
		self.turn = 1

		self.first_time = 0

		# Load images
		self.loadImages()

		self.subwindows = []
		
		
		# Load up the canvas, load up bg
		self._canvas = gui.get_canvas()	      
		self.bg_image = self._canvas.create_image(0,0,image=self.icons['bg'],anchor='nw')

		# Bind text for cash display
		self.cashLabel = gui.get_cashlabel()
		self.cashcontents = StringVar()
		self.cashLabel['textvariable'] = self.cashcontents
		self.cashcontents.set(' $ ' + str(self.cash))

		# Bind mouse motion
		self._canvas.bind("<ButtonPress-1>", xy)
		self._canvas.bind("<ButtonPress-3>", xy)
		self._canvas.bind("<ButtonRelease-3>", lambda x: self.submenuother())

		# Draw cities
		self.city_images = {}
		self.city_text = {}
		for city in self.economy.GetCities():
			self.DrawCity(city)

		# Initialize a dictionary of lines objects
		self.E_lines = { }
		self.E_text = {}
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

		# Create initial submenu
		self.submenu =	CanvasSubMenu(100,100,
			      self._canvas,0,
			      self.icons)

		#Tutorial beginings
		messagebox.showinfo('Welcome to Telecom Tycoon',message = 'Lets get started, shall we?')
		messagebox.showinfo(message='Right click anywhere to begin')
		
	def Tutorial(self):
		global RightCounter
		RightCounter+=1
		messagebox.showinfo(message='Please select the add node button.')
		messagebox.showinfo(message='This should be the green plus in the sub-menu.')
		messagebox.showinfo(message='This NETWORK NODE represents\na bandwidth origin.')
		self.first_time = 1

	# Draw cities
	def DrawCity(self,city):
		# Get the coordinates of the city.
		(x,y) = city.GetCoord()

		self._canvas.create_oval(x-100,y-100,x+100,y+100,outline='blue')

		# Draw different pictures for different populations
		vspace = 0
		if city.GetPopulation() >= 1000000:
			self.city_images[city.GetName()] =  self._canvas.create_image(x,y,
										      image=self.icons['big_city'],
										      activeimage=self.icons['big_city_active'],
										      anchor='center')
			vspace = 80

		elif 50000 <= city.GetPopulation() < 1000000:
			self.city_images[city.GetName()] =  self._canvas.create_image(x,y,
										      image=self.icons['city'],
										      activeimage=self.icons['city_active'],
										      anchor='center')
			vspace = 70

		elif city.GetPopulation() < 50000:
			self.city_images[city.GetName()] =  self._canvas.create_image(x,y,
										      image=self.icons['town'],
										      activeimage=self.icons['town_active'],
										      anchor='center')
			vspace = 50

		
		self.city_text[city.GetName()] = self._canvas.create_text(x,y + vspace,
							     text=city.GetName(),
							     anchor='center',fill='white')

	

		# Attach event binding
		self._canvas.tag_bind(self.city_images[city.GetName()],"<ButtonRelease-1>", lambda x: self.DispCity(city))

	# Display city data
	def DispCity(self,city):
		(i,o) = city.GetSupply()
		messagebox.showinfo('City Info','Population:  %0.0f' % city.GetPopulation() + '\nDownlink Supply: %0.0f' %(o / 1000000) + ' Mbit/s' + '\nUplink Supply: %0.0f' %(i / 1000000) + ' Mbit/s')
		
	def NewEdgeCanvas(self,edge):
		(x1,y1) = self.gameNetwork.V_coord[edge[0]]
		(x2,y2) = self.gameNetwork.V_coord[edge[1]]

		# Color code nodes by operation
		if len(self.gameNetwork.E_items[edge]) > 0:
			fillcolor = 'green'
		else:
			fillcolor='black'

		x1 = x1 + 5 * math.cos(math.atan2(y2-y1,x2-x1) + math.pi/2)
		x2 = x2 + 5 * math.cos(math.atan2(y2-y1,x2-x1) + math.pi/2)
		y1 = y1 + 5 * math.sin(math.atan2(y2-y1,x2-x1) + math.pi/2)
		y2 = y2 + 5 * math.sin(math.atan2(y2-y1,x2-x1) + math.pi/2)

		# Add a little bit of separation so bidirectional links can be selected.
		self.E_lines[edge] = self._canvas.create_line(x1,y1,x2,y2,
							      fill=fillcolor,activefill='purple',width=3)
		(mid_x,mid_y) = midpoint((x1,y1),(x2,y2))

		# Draw indicator for bidirectional links
		(mid2_x,mid2_y) = midpoint((mid_x,mid_y),(x2,y2))
		self.E_direction_marker[edge] = [self._canvas.create_line(mid2_x,mid2_y,
									 mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) + 3.5 * math.pi/4),
									 mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) + 3.5 * math.pi/4),
									 fill='blue',width=2),
						 self._canvas.create_line(mid2_x,mid2_y,
									  mid2_x + 10 * math.cos(math.atan2(y2-y1,x2-x1) - 3.5 * math.pi/4),
									  mid2_y + 10 * math.sin(math.atan2(y2-y1,x2-x1) - 3.5 * math.pi/4),
									  fill='blue',width=2)]

		# Draw distances at edges
		self.E_text[edge] = self._canvas.create_text(mid_x + 20 * math.cos(math.atan2(y2-y1,x2-x1) - math.pi / 2),
							     mid_y + 30 * math.sin(math.atan2(y2-y1,x2-x1) - math.pi / 2),
							     anchor='center',text=('%0.2f' % (self.gameNetwork.E_lengths[edge]) + ' km'),
							     fill='white')
							     
		# Attach mouse events:
		self._canvas.tag_bind(self.E_lines[edge],"<ButtonRelease-3>", lambda x: self.submenuLink(edge))
		self._canvas.tag_bind(self.E_lines[edge],"<ButtonRelease-1>", lambda x: self.editLink(edge))

	# Delete a link from the canvas
	def DelLinkCanvas(self,link):
		self._canvas.delete(self.E_lines[link])
		for i in self.E_direction_marker[link]: self._canvas.delete(i)
		self._canvas.delete(self.E_text[link])

	# Function adds new node imagery dictionaries and canvas
	def NewNodeCanvas(self,node):
		(x,y) = self.gameNetwork.V_coord[node]
		self.V_images[node] = self._canvas.create_image(x,y,
								image=self.icons['node'],
								activeimage=self.icons['node_active'],
								anchor='center')
		self.V_text[node] = self._canvas.create_text(x + 30,y,
							     text=(self.gameNetwork.V_name[node]),
							     anchor='w',fill='white')
		# Attach mouse events to each node iamge
		self._canvas.tag_bind(self.V_images[node],"<ButtonRelease-1>", lambda x: self.displayNode(node))
		self._canvas.tag_bind(self.V_images[node],"<ButtonRelease-3>", lambda x: self.submenuNode(node))

	# Delete a node from canvas
	def DelNodeCanvas(self,node):
		self._canvas.delete(self.V_images[node])
		self._canvas.delete(self.V_text[node])

	# Creates an instance of a window to display the node data.
	def displayNode(self,node):
		self.V_displays.add(node)
		maxcap = self.gameNetwork.MaxCapAtNode(node)
		cap_frac = (maxcap - self.gameNetwork.cap_at_node_cached[node]) / (maxcap + 0.00000001)
		self.subwindows.append(NodeDisplay(self._canvas.canvasx(lastx),
						   self._canvas.canvasy(lasty),
						   self._canvas,
						   node,
						   self.gameNetwork,
						   self.icons,
						   gui.GetRoot(),
						   self.inventory,
						   cap_frac))

	# Open the edit link menu
	def editLink(self,edge):
		new = EditLink(gui.GetRoot(),self.inventory,edge,self.gameNetwork)

	# Display a right-click submenu on the canvas
	def submenuNode(self,node):
		global lastx, lasty
		# Close the previous instance of the menu
		self.submenu.close()
		del self.submenu
		self.submenu = CanvasSubMenu(self._canvas.canvasx(lastx),
					     self._canvas.canvasy(lasty),
					     self._canvas,node,
					     self.icons,nodeflag=1)
		
	# Display a submenu for clicking a link
	def submenuLink(self,edge):
		global lastx, lasty
		self.submenu.close()
		del self.submenu
		self.submenu = CanvasSubMenu(self._canvas.canvasx(lastx),
					     self._canvas.canvasy(lasty),
					     self._canvas,edge,
					     self.icons,linkflag=1)

	# Display submenu for other clicks
	def submenuother(self):
		global lastx, lasty
		global RightCounter
		RightCounter=2
		# Don't open a submenu on top of a node or edge one.
		distance = dist(self._canvas.canvasx(lastx),self._canvas.canvasy(lasty),self.submenu.x,self.submenu.y)
		if distance > 10:
			self.submenu.close()
			del self.submenu
			self.submenu = CanvasSubMenu(self._canvas.canvasx(lastx),
						     self._canvas.canvasy(lasty),
						     self._canvas,0,
						     self.icons)
	# Loads a dictionary of imags
	def loadImages(self):
		self.icons = { }
		self.icons['sstower'] = PhotoImage(file = 'images/tower.gif')
		self.icons['sstower_active'] = PhotoImage(file = 'images/tower_active.gif')
		self.icons['node'] = PhotoImage(file = 'images/node.gif')
		self.icons['node_active'] = PhotoImage(file = 'images/node_active.gif')
		self.icons['bg'] = PhotoImage(file = 'images/terrain.gif')
		self.icons['close']= PhotoImage(file = 'images/close.gif')
		self.icons['close_active']= PhotoImage(file = 'images/close_active.gif')
		self.icons['addbutton']= PhotoImage(file = 'images/addbutton.gif')
		self.icons['addbutton_active']= PhotoImage(file = 'images/addbutton_active.gif')
		self.icons['notify']= PhotoImage(file = 'images/notify.gif')
		self.icons['backpane']= PhotoImage(file = 'images/backpane.gif')
		self.icons['city']= PhotoImage(file = 'images/city-icon.gif')
		self.icons['city_active']= PhotoImage(file = 'images/city-icon_active.gif')
		self.icons['big_city']= PhotoImage(file = 'images/big_city.gif')
		self.icons['big_city_active']= PhotoImage(file = 'images/big_city_active.gif')
		self.icons['town']= PhotoImage(file = 'images/town.gif')
		self.icons['town_active']= PhotoImage(file = 'images/town_active.gif')

		# Canvas submenu
		self.icons['addnode']= PhotoImage(file = 'images/canvassubmenu/addnode.gif')
		self.icons['addnode_active']= PhotoImage(file = 'images/canvassubmenu/addnode_active.gif')
		self.icons['addnode_inactive']= PhotoImage(file = 'images/canvassubmenu/addnode_inactive.gif')
		self.icons['delnode']= PhotoImage(file = 'images/canvassubmenu/delnode.gif')
		self.icons['delnode_active']= PhotoImage(file = 'images/canvassubmenu/delnode_active.gif')
		self.icons['delnode_inactive']= PhotoImage(file = 'images/canvassubmenu/delnode_inactive.gif')
		self.icons['addlink']= PhotoImage(file = 'images/canvassubmenu/newlink.gif')
		self.icons['addlink_active']= PhotoImage(file = 'images/canvassubmenu/newlink_active.gif')
		self.icons['addlink_inactive']= PhotoImage(file = 'images/canvassubmenu/newlink_inactive.gif')
		self.icons['dellink']= PhotoImage(file = 'images/canvassubmenu/dellink.gif')
		self.icons['dellink_active']= PhotoImage(file = 'images/canvassubmenu/dellink_active.gif')
		self.icons['dellink_inactive']= PhotoImage(file = 'images/canvassubmenu/dellink_inactive.gif')

	def do_turn(self):
		# Message display
		if self.first_time==1 and self.gameNetwork.vertex_counter==2:
			messagebox.showinfo(message='You will need to create another\nif your current node\nis not near a city.')
			self.first_time=2

		if self.first_time==2 and self.gameNetwork.vertex_counter==3:
			messagebox.showinfo(message='Right click on your new node\n')
			messagebox.showinfo(message='Then left click the connection button\n')
			messagebox.showinfo(message='Again, this should be a green plus\n')
			messagebox.showinfo(message='Double-click on your\nfirst node to \ncreate a connection.')
			self.first_time = 3

		if self.first_time==0:
			if RightCounter==2:
				self.Tutorial()
		
		# Tried playing. Setting -50000 was too hard.
		if self.cash < -100000:
			messagebox.showinfo(message='YOU LOSE. YOU WENT TOO FAR INTO DEBT.\nGAME OVER')
			quit()
		# Deal with action queue.
		global action_q
		
		# Process each action
		while len(action_q) > 0:
			action = action_q.pop(0)
			self.processAction(action)

		total_maintCost = 0
		# Refresh ll stat windows, which will be inaccurate
		for window in self.subwindows:
			if not window.Closed():
				maxcap = self.gameNetwork.MaxCapAtNode(window.node)
				cap_frac = (maxcap - self.gameNetwork.cap_at_node_cached[window.node]) / (maxcap + 0.00000001)
				window.refresh(self.inventory,
					       cap_frac)
				# Note avoiding divide by zero error above
			else:
				self.subwindows.remove(window)

		# Updat all of the items at nides for a turn.
		for nodeKey in self.gameNetwork.V_items.keys():

			# Pay rent per step. This amounts to $1000 a month
			total_maintCost = total_maintCost + 1.38

			if not self.gameNetwork.NodeOperational(nodeKey):
				try: 
					self.V_notify[nodeKey]
				except:
					self.V_notify[nodeKey] = self._canvas.create_image(self.gameNetwork.V_coord[nodeKey][0] - 8,
											   self.gameNetwork.V_coord[nodeKey ][1] - 16,
											   image=self.icons['notify'],
											   anchor='se')
			else:
				try: self._canvas.delete(self.V_notify[nodeKey])
				except: pass
				
			for item in self.gameNetwork.V_items[nodeKey]:
				fail = item.Update()
				# Add a message telling what failed and where, if it did.
				if fail == True:
					self._messages.append(item.GetName() + " failed at " + self.gameNetwork.V_name[nodeKey])	  
				if item.Operating():
					# Record maintennace cost
					total_maintCost = total_maintCost + item.GetMaintenance()

					# Service items that are within node items.
					for subitem in item.GetInventory():
						fail_subitem = subitem.Update()
						# Add a message telling what failed and where, if it did.
						if fail_subitem == True:
							self._messages.append(subitem.GetName() + " failed at " + self.gameNetwork.V_name[nodeKey])	  
						if subitem.Operating():
							# Record maintennace cost
							total_maintCost = total_maintCost + subitem.GetMaintenance()
	
		# Update items at edges
		for edgekey in self.gameNetwork.E_items.keys():
			if len(self.gameNetwork.E_items[edgekey]) > 0:
				self._canvas.itemconfigure(self.E_lines[edgekey],fill='green')
			else:
				self._canvas.itemconfigure(self.E_lines[edgekey],fill='black')
			for item in self.gameNetwork.E_items[edgekey]:
				fail = item.Update()
				# Add a message telling what failed and where, if it did.
				if fail == True:
					self._messages.append(item.GetName() + " failed ")
					
				else:
					# Record maintennace cost
					total_maintCost = total_maintCost + item.GetMaintenance()

				if not item.Operating():
					self._canvas.itemconfigure(self.E_lines[edgekey],fill='red')
				
		
		# Update how much money to make:
		revenue = 0

		self.gameNetwork.CapReset()
		for city in self.economy.GetCities():
			city.SetSupply(self.gameNetwork.CapAtCoord(city.GetCoord(),self.economy.GetCitiesCoord()))
			#print(city.GetName() + ': ' + str(city.GetSupply()))

			# Add revenue
			revenue = revenue + city.Revenue()
		
		self.gameNetwork.CapCache()
		
		# Update the economy
		self.economy.Update(self.turn)


		# Update game parameters
		self.cash = self.cash - total_maintCost + revenue

		# A turn corresponds to one hour
		self.turn = self.turn + 1

		tempstr = 'Cash:  $ %0.2f' % self.cash + '  Cost per week: $%0.2f' % (total_maintCost * 24 * 7)
		tempstr = tempstr + '  Weekly Revenue: $%0.2f' % (revenue * 24 * 7)
		tempstr = tempstr + '  Net Profit per week: $ %0.2f' % ((-total_maintCost + revenue) * 7 * 24)
		tempstr = tempstr + '\nTime: %02d' % (self.turn % 24) + ':00'
		tempstr = tempstr + '  Day: ' + str(self.turn // 24 % 365)
		tempstr = tempstr + ' Year: ' + str(self.turn  //  (365 * 24))
		self.cashcontents.set(tempstr)
		
		# Empty the message stack to the user.
		while len(self._messages) > 0:
			messagebox.showinfo("Message",self._messages.pop(0),
					    icon='warning')

	# Process individual action from the action stack
	def processAction(self,action):
		# print(action)

		# DIfferent actions are possible based on the item at index 0.

		if action[0] == 'addnode':
			coord = action[1][0]
			name = action[1][1]
			# add the node
			node = self.gameNetwork.NewNode(coord,name,[])
			self.NewNodeCanvas(node)
			return

		elif action[0] == 'addlink':
			node = action[1][0]
			pt = action[1][1]
			dist = 200

			(closestNode, distance) = self.gameNetwork.ReturnClosePoint(pt)

			# Return early if the selected link is invaiid. 
			if closestNode == node or distance > 100:
				return

			# ask if the user wants to add the edge.
			answer = messagebox.askyesno('Question',
						     'Add link from ' + self.gameNetwork.V_name[node] + ' to ' + self.gameNetwork.V_name[closestNode] + '?')
			if answer == False:
				return
			else:
				self.gameNetwork.AddEdgeID(node,closestNode,[])
				self.NewEdgeCanvas((node,closestNode))
				return

		elif action[0] == 'delnode':
			node_to_del = action[1][0]
			answer = messagebox.askyesno('Warning',
						     'Are you sure you want to delete ' + self.gameNetwork.V_name[node_to_del] + ' and all of its contents?')
			
			if answer:
				# Start by deleting all links attached to the node.
				# Copy the list so you can iterate over it without changing size.
				adj = copy.deepcopy(self.gameNetwork.graph.vertices())

				for i in adj:
					# Both ways
					try:
						self.gameNetwork.DelLink((node_to_del,i))
						self.DelLinkCanvas((node_to_del,i))

						self.gameNetwork.DelLink((i, node_to_del))
						self.DelLinkCanvas((i, node_to_del))
					except:
						# Kinda like "on error resume next"
						continue

				new_inv = self.gameNetwork.DelNode(node_to_del)
				self.DelNodeCanvas(node_to_del)
				return

		elif action[0] == 'dellink':
			link_to_del = action[1][0]
			answer = messagebox.askyesno('Warning',
						     'Are you sure you want to delete this link and all of its contents?')
			if answer:
				self.gameNetwork.DelLink(link_to_del)
				self.DelLinkCanvas(link_to_del)
				return
			

		elif action[0] == 'subtractcash':
			self.cash = self.cash - action[1][0]
			return

		# Change the inventory to the incoming inventory.
		elif action[0] == 'inv':
			"""
			# Clear the inventory
			while len(self.inventory) > 0:
				self.inventory.pop()
				
			for item in action[1]:
				self.inventory.append(copy.copy(item))
				store.refresh_flag = True
				editnode.refresh_flag = True
			"""
			self.inventory = copy.deepcopy(action[1])
			global gui
			gui.inventory = self.inventory

			


def rgb_to_color(r, g, b):
    """
		Utility to generate a Tk color rgb string from	integer r, g, b,
		where 0 <= r, g, b <= 1
		
		Use as in
	agentsim.gui.get_canvas().create_oval(10, 20, 30, 40,
		fill=agentsim.rgb_to_color(.8, .8, 0) )
		"""
	
    return '#{0:02x}{1:02x}{2:02x}'.format(
										   int((r * 255) % 256), int((g * 255) % 256), int((b * 255) % 256), )

# Find the midpoint between two points
def midpoint(pt1,pt2):
	(x1,y1) = pt1
	(x2,y2) = pt2
	return ((x1+x2)//2,(y1+y2)//2)


