import random

class Item:
    """
    Test item operation:

    >>> testItem = Item("ITEM",20000,1,0,100,100,100)
    >>> testItem.SetOperating()
    >>> testItem.GetCost() == 20000
    True
    >>> testItem.Operating() == True
    True
    """
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint):
        self.name = name
        self.cost = cost
        # Note the reliability constant is a number between 0 and 1. 1 is most reliable
        self.reliability_constant = rel
        self.icon = icon
        # Lifespan is the number of turns the item will generally last. 
        self.lifespan = lifespan
        self.maintenance_budget = maintenance
        self.suggested_maint_budget = sug_maint

        # Note: New items are set operational by default.
        self.operating = True
        # Age is the number of turns the item has been operating for.
        self.age = 0

    # Get name
    def GetName(self):
        return self.name

    # Get cost
    def GetCost(self):
        return self.cost

    # Check operating status
    def Operating(self):
        return self.operating

    # Make the item operational
    def SetOperating(self):
        self.operating = True

    # Make the item fail
    def SetFail(self):
        self.operating = False

    # Tells whether or not the item is beyond its operating lifespan.
    def OverLifespan(self):
        if self.age >= self.lifespan:
            return True
        else:
            return False

    # Updates the item for every turn, and calculates potential failure
    # Returns True if the item failed.
    def Update(self):

        self.age = self.age + 1
        
        # If the item already failed, continue to return it did.
        if self.Operating() == False:
            return True


        # Calculate failure chance. Tested the algorithm with a TEST program.
        # This failure chance is only for a failure by natural causes. 
        random.seed()
        chance = random.random() / (self.reliability_constant * 20) + (self.age / self.lifespan / (self.maintenance_budget / self.suggested_maint_budget)) * random.random()
        if chance >= 1:
            self.SetFail()
            return True
        return False

    # This function is used to age itmes which are not deployed. 
    # Non deployed items shouldn't fail.
    def Age(self):
        self.age = self.age + 1

    # Print out the item
    def print(self):
        print(self.name + " object.")

# Structural Types

class Structure(Item):
    """
    TESTS:
    Argument order: (name,cost,re,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,,max_length,radio_type)

    >>> newTower = Tower("Tower",30000,1,1,300,1000,1000,50000,6,1,50)
    >>> newRadio = Radio("Alcatel MDR 8502 E-8",30000,1,1,200,100,100,12,1,1,100,"DS1")
    >>> newTower.AddItem(newRadio)
    True
    >>> len(newTower.GetInventory()) == 1
    True
    >>> a = newTower.RemoveItem(0)
    >>> len(newTower.GetInventory()) == 0
    True
    >>> a.GetName()
    'Alcatel MDR 8502 E-8'
    
    Test buildings and max slots.
    >>> newBuilding = Building("Building",30000,1,1,300,1000,1000,50000,6)
    >>> newWire = Wired("Fujitsu Flashwave E4500",30000,1,1,200,100,100,12,1,1,100,"Fiber Optic 1310/1550 nm")
    >>> newBuilding.AddItem(newWire)
    True
    >>> newBuilding.AddItem(a)
    True
    >>> newBuilding.AddItem(a)
    True
    >>> newBuilding.AddItem(a)
    True
    >>> newBuilding.AddItem(a)
    True
    >>> newBuilding.AddItem(a)
    True

    Should not be able to add next:
    >>> newBuilding.AddItem(a)
    False

    """
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots):
        super(Structure,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint)
        # Set the cost of the structure's foundation..
        self.foundation_cost = foundation_cost
        # This is the list of objects at a structure.
        self.Inventory = []
        # Slots are the max number of items you can have in the structure.
        self.slots = slots
    
    # Returns false if the item was not added.
    def AddItem(self, ObjectToAdd):
        # Note that 0 counts as a slot in the inventory list
        if len(self.Inventory) < self.slots:
            self.Inventory.append(ObjectToAdd)
            return True
        else:
            return False

    # Returns the inventory
    def GetInventory(self):
        return self.Inventory

    # Remove an item from the inventory and return it.
    def RemoveItem(self, index):
        if len(self.Inventory):
            return self.Inventory.pop(index)
        else:
            return None

class Building(Structure):
    def __init(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots):
        super(Building,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots)

class Tower(Structure):
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots,tower_type,tower_height):
        super(Tower,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots)
        self.tower_height = tower_height
        self.tower_type = tower_type


# Netowrk types:

class Network(Item):
    """
    Tests:

    >>> newRouter = Router("HP Router",10000,1,1,100,200,200,10000,500,1,10)
    >>> newRouter.GetCapacity() == 500
    True
    >>> newRouter.SetCapacity(800)
    True
    >>> newRouter.GetCapacity() == 800
    True
    >>> newRouter.SetCapacity(100000)
    False
    >>> newRouter.GetCapacity() == newRouter.GetMaxCapacity()
    True
    """

    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power):
        super(Network,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint)
        self.max_capacity = max_capacity
        self.target_capacity = target_capacity
        self.power_consumption = power

    # Get currently set capacity
    def GetCapacity(self):
        return self.target_capacity

    # Get max capacity
    def GetMaxCapacity(self):
        return self.max_capacity

    # Sets the capacity allotted to the particular network component. Cannot exceed max.
    def SetCapacity(self,target):
        self.target_capacity = target
        if self.target_capacity > self.max_capacity:
            self.target_capacity = self.max_capacity
            return False
        return True

class Router(Network):
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,service_range):
        super(Router,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power)
        self.service_range = service_range

class PointToPoint(Network):
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length):
         super(PointToPoint,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power)
         # Maximum length of a point to point connection before a repeater is needed.
         self.max_length = max_length

class Radio(PointToPoint):
    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length,radio_type):
        super(Radio,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length)
        # Radio types are ...
        self.radio_type = radio_type
    def GetType(self):
        return self.radio_type

class Wired(PointToPoint):

    def __init__(self,name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length,wire_type):
        super(Wired,self).__init__(name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length)
        # Wire types are ...
        self.wire_type = wire_type

    def GetType(self):
        return self.wire_type

if __name__ == "__main__":
    import doctest
    doctest.testmod()
