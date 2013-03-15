import random

class Item:
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint):
        self.cost = cost
        # Note the reliability constant is a number between 1 and 100. 100 is most reliable
        self.reliability_constant = rel
        self.icon = icon
        # Lifespan is the number of turns the item will generally last. 
        self.lifespan = lifespan
        self.maintenance_budget = maintenance
        self.suggested_maint_budget = sug_maint
        self.operating = True
        # Age is the number of turns the item has been operating for.
        self.age = 0

    # Check operating status
    def GetOperatingStatus(self):
        return self.operating

    # Make the item operational
    def SetOperating(self):
        self.operating = true

    # Make the item fail
    def SetFail(self):
        self.operating = False

    # Updates the item for every turn, and calculates potential failure
    # Returns True if the item failed.
    def Update(self):
        random.seed()

        self.age = self.age + 1
        
        # Calculate failure chance. Maybe a better algorithm could be used? 
        # This failure chance is only for a failure by natural causes. 
        chance = random.random() / self.reliability_constant + (self.age / self.lifespan / (self.maintenance_budget / self.suggested_maint_budget))
        if chance >= 0.5:
            self.SetFail()
            return True
        
        return False

# Structural Types

class Structure(Item):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint)
        # Set the cost of the structure's foundation.
        self.foundation_cost = foundation_cost

class Tower(Structure):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,tower_type,tower_height):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,foundation_cost)
        self.tower_height = tower_height
        self.tower_type = tower_type


# Netowrk types:

class Network(Item):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint)
        self.max_capacity = max_capacity
        self.target_capacity = target_capacity
        self.power_consumption = power

    # Sets the capacity allotted to the particular network component. Cannot exceed max.
    def SetCapacity(self,target):
        self.target_capacity = target
        if self.target_capacity > self.max_capacity:
            self.target_capacity = self.max_capacity

class Router(Network):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,service_range):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power)
        self.service_range = service_range

class PointToPoint(Network):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,max_length):
        super().init(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power)
        # Maximum length of a point to point connection before a repeater is needed.
        self.max_length = max_length

class Radio(PointToPoint):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,radio_type):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power)
        # Radio types are ...
        self.radio_type = radio_type

class Wired(PointToPoint):
    def __init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power):
        super().__init__(self,cost,rel,icon,lifespan,maintenance,sug_maint,max_capacity,target_capacity,power,wire_type)
        # Wire types are ...
        self.wire_type = wire_type
