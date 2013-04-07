# This class is for the game economic system. 
# This system determines supply and demand of cities in 
# the network. It also can update.

# NOTE: THIS CLASS IS CURRENTLY A STUB

import math
import random

from city import *

# This is a library which implements linear and quadratic curves.
from curves import *

class Economic():

    def __init__(self,cities_list):
        # Cities list is a list of 
        # City objects that are part of the economic system.
        self.cities = cities_list

    # Accessors:
    def GetCities(self):
        return self.cities

    # Step functions
    def Update(self,turn):
        # This function is called once per step. It updates the system.
        for city in self.cities:
            city.Update(turn)

    def GetDemand(self,x,y):
        # Given a coordinate point, this function returns the demand
        # for bandwidth at the location. 

        # It should find the nearest population center, then subtract  a "fade factor"
        # depending on the distnace from the popualtion center. Shouldn't be negative.

        # Each city should have a demand curve. This function returns 
        # the curve, which is the downward sloping half of a quadratic.
        return None
