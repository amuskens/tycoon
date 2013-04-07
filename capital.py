import random
import math
import copy

class Item:
    """
    Test item operation:

    >>> testItem = Item(("ITEM",20000,1,0,100,100,100))
    >>> testItem.SetOperating()
    >>> testItem.GetCost() == 20000
    True
    >>> testItem.Operating() == True
    True
    """
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint) = inList
        self.name = name
        self.cost = float(cost)
        # Note the reliability constant is a number between 0 and 1. 1 is most reliable
        self.reliability_constant = float(rel)
        self.icon = icon
        # Lifespan is the number of turns the item will generally last. 
        self.lifespan = float(lifespan)
        self.maintenance_budget = float(maintenance)
        self.suggested_maint_budget = float(sug_maint)

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

    # Get lifespan
    def GetLifespan(self):
        return self.lifespan

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

    # Set the maintenance budget
    def SetMaintenance(self,num):
        if num > 0:
            self.maintenance_budget = float(num)
        else:
            self.maintenance_budget = 0.000001
        

    # Get maintennace budget
    def GetMaintenance(self):
        return (self.maintenance_budget)

    # Get suggested maintenance
    def SugMaintenance(self):
        return (self.suggested_maint_budget)

    # Updates the item for every turn, and calculates potential failure
    # Returns True if the item failed.
    def Update(self):

        self.age = self.age + 1
        
        # If the item already failed, continue to return it did.
        if self.Operating() == False:
            return False


        # Calculate failure chance. Tested the algorithm with a TEST program.
        # This failure chance is only for a failure by natural causes. 
        random.seed()
        chance = random.random() / (self.reliability_constant * 20) + (self.age / (self.lifespan + 0.1 * self.reliability_constant * self.lifespan) / (self.maintenance_budget / self.suggested_maint_budget) * random.random())
        if chance >= 1:
            self.SetFail()
            return True
        return False

    # This function is used to age itmes which are not deployed. 
    # Non deployed items shouldn't fail.
    def Age(self):
        self.age = self.age + 1

    def GetAge(self):
        return self.age

    # Print out the item
    def print(self):
        print(self.name + " object.")
        
    def GetInfo(self):
        return ''

# Structural Types

class Structure(Item):
    """
    TESTS:
    Argument order: (name,cost,re,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,,max_length,radio_type)

    >>> newTower = Tower(("Tower",30000,1,1,300,1000,1000,50000,6,1,50))
    >>> newRadio = Radio(("Alcatel MDR 8502 E-8",30000,1,1,200,100,100,12,1,1,100,"DS1",2000,1500,10000))
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
    >>> newBuilding = Building(("Building",30000,1,1,300,1000,1000,50000,6))
    >>> newWire = Wired(("Fujitsu Flashwave E4500",30000,1,1,200,100,100,12,1,1,100,"Fiber Optic 1310/1550 nm",99))
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
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots,linkslots) = inList
        super(Structure,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint))
        # Set the cost of the structure's foundation..
        self.foundation_cost = foundation_cost
        # This is the list of objects at a structure.
        self.Inventory = []
        # Slots are the max number of physical items you can have in the structure.
        self.slots = int(slots)
        # Link slots are for items in edges.
        self.link_slots = int(linkslots)
        self.filled_link_slots = 0

    def GetFoundationCost(self):
        return self.foundation_cost
    
    # Returns false if the item was not added.
    def AddItem(self, ObjectToAdd):
        # Note that 0 counts as a slot in the inventory list
        if len(self.Inventory) < self.slots:
            self.Inventory.append(copy.deepcopy(ObjectToAdd))
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

    def type(self):
        return("Structure")

    # Accessors:
    def GetMaxLinkSlots(self):
        return self.link_slots

    def GetCurLinkSlots(self):
        return self.filled_link_slots

    # Add a link
    def AddLink():
        if self.filled_link_slots < self.link_slots:
            self.link_slots = self.link_slots + 1
            return True
        else:
            return False

    # Remove a link
    def RemoveLink():
        if self.fille_link_slots > 0:
            self.link_slots = self.link_slots - 1
            return True
        else:
            return False

class Building(Structure):
    def __init(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots,linkslots) = inList
        super(Building,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots,linkslots))

    def StructType(self):
        return 'Building'

    def GetInfo(self):
        item = self
        tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
        tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
        tempstr = tempstr + '\nFoundation Cost: $ %0.2f' % float(item.GetFoundationCost())
        tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
        tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
        tempstr = tempstr + '\nBuild slots: ' + str(item.slots)
        tempstr = tempstr + '\nAge: ' + str(item.GetAge())
        return tempstr


class Tower(Structure):
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,slots,tower_type,tower_height) = inList
        # Towers generally have 0 item slots, but have link slots.
        super(Tower,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost,0,slots))
        self.tower_height = tower_height
        self.tower_type = tower_type

    def StructType(self):
        return 'Tower'
        
    def GetTowerType(self):
        return self.tower_type

    def GetTowerHeight(self):
        return self.tower_height

    def GetInfo(self):
        item = self
        tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
        tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
        tempstr = tempstr + '\nFoundation Cost: $ %0.2f' % float(item.GetFoundationCost())
        tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
        tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
        tempstr = tempstr + '\nTower Type: ' + item.GetTowerType()
        tempstr = tempstr + '\nTower Height: ' + item.GetTowerHeight() + ' m'
        tempstr = tempstr + '\nBuild slots: ' + str(item.slots)
        tempstr = tempstr + '\nAge: ' + str(item.GetAge())
        return tempstr
	


# Netowrk types:

class Network(Item):
    """
    Tests:

    >>> newRouter = Router(("HP Router",10000,1,1,100,200,200,10000,500,1,10))
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

    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power) = inList
        super(Network,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint))
        self.max_capacity = float(max_capacity)
        self.target_capacity = float(target_capacity)
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
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,service_range) = inList
        super(Router,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power))
        self.service_range = service_range

    def type(self):
        return("Router")

    def GetInfo(self):
        item = self
        tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
        tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
        tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
        tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
        tempstr = tempstr + '\nMaximum Capacity: %0.2f' % (float(item.GetMaxCapacity()) / 1000000) + ' megabits per second'
        tempstr = tempstr + '\nAge: ' + str(item.GetAge())
        return tempstr

class PointToPoint(Network):
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length) = inList
        super(PointToPoint,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power))
        # Maximum length of a point to point connection before a repeater is needed.
        self.max_length = float(max_length)

    def GetMaxLength(self):
        return self.max_length

class Radio(PointToPoint):
    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length,radio_type,radio_frequency,freq_lo,freq_hi) = inList
        super(Radio,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length))
        # Radio types are ...
        self.radio_type = radio_type
        self.frequency = float(radio_frequency)

        # Allowed frequencies is a range in a tuple. E.g. (2000,10000)
        self.allowed_freq = (float(freq_lo),float(freq_hi))

    def type(self):
        return("Radio")

    def RadioGetType(self):
        return self.radio_type

    # Check if a frequency is allowed on the radio.
    def FreqAllowed(self,freq):
        if self.allowed_freq[0] <= freq <= self.allowed_freq:
            return True
        else:
            return False

    def GetFreqRange(self):
        return self.allowed_freq
    
    # Set the radio broadcast frequency
    def SetFreq(self,freq):
        if self.FreqAllowed(freq):
            self.radio_frequency = float(freq)
            return True
        else:
            return False

    # Info
    def GetInfo(self):
        item = self
        tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
        tempstr = tempstr + '\nCost: $ ' + "%0.2f" % item.GetCost()
        tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
        tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
        tempstr = tempstr + '\nMaximum Capacity: %0.2f' % (float(item.GetMaxCapacity()) / 1000000) + ' megabits per second'
        tempstr = tempstr + '\nMaximum Link Length: ' + str(item.GetMaxLength()) + ' km'
        tempstr = tempstr + '\nFrequency Range: %0.2f' % (float(item.GetFreqRange()[0])) + ' MHz to %0.2f' % (float(item.GetFreqRange()[1])) + ' MHz'
        tempstr = tempstr + '\nRadio Type: ' + item.RadioGetType()
        tempstr = tempstr + '\nAge: ' + str(item.GetAge())
        return tempstr

    """
    Note: Terrain and weather should affect radio connection reliability.
    This to be implemented later.

    """
        

class Wired(PointToPoint):

    def __init__(self,inList):
        (name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length,wire_type,attenuation) = inList
        super(Wired,self).__init__((name,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length))
        # Wire types are ...
        self.wire_type = wire_type

        # Signal attenuation constant on wire. Between 1 and 1000. 1000 is the worst.
        self.attenuation = float(attenuation)
        self.cur_max_capacity = float(max_capacity)

    def type(self):
        return("Wired")

    def WiredGetType(self):
        return self.wire_type

    def GetAttenuation(self):
        return self.attenuation

    # Returns the maximum bandwidth at a certain distance as determined
    # by the attenuation of the wire
    def DistCapacity(self,dist):
        return self.max_capacity - 100000 * (dist / (self.max_length / self.attenuation))

    # Set the target capacity of the wire
    def SetCapacity(self,cap):
        if cap <= self.cur_max_capacity:
            self.target_capacity = cap
            return True
        else:
            return False

    # Set the current max capacity of the wire based on distance and attenuation
    def SetWireMaxCapacity(self,dist):
        self.cur_max_capacity = self.DistCapacity(dist)

    def GetInfo(self):
        item = self
        tempstr = 'Item Description: \n' + 'Name: ' + item.GetName()
        tempstr = tempstr + '\nCost per km: $ ' + "%0.2f" % item.GetCost() + ' / km'
        tempstr = tempstr + '\nSuggested maintenance budget: $ %0.2f'% (item.SugMaintenance() * 24 * 7) + ' per week'
        tempstr = tempstr + '\nProjected Lifespan: %0.2f' % (item.GetLifespan() / 365 / 24) + ' years'
        tempstr = tempstr + '\nOptimal Maximum Capacity: %0.2f' % (float(item.GetMaxCapacity()) / 1000000) + ' megabits per second'
        tempstr = tempstr + '\nMaximum Link Length: ' + str(item.GetMaxLength()) + ' km'
        tempstr = tempstr + '\nCapacity for 1 km: %0.2f' % (float(item.DistCapacity(1) / 1000000)) + ' megabits per second'
        tempstr = tempstr + '\nAttenuation: %0.2f' % (float(item.GetAttenuation()) / 100) + ' dB'
        tempstr = tempstr + '\nType: ' + item.WiredGetType()
        tempstr = tempstr + '\nAge: ' + str(item.GetAge())
        return tempstr
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
