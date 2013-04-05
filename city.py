# This class instantiates city objects

import random
import math

from curves import *

class City():

    # Initialize a new city
    def __init__(self,name,x,y,population=1000,growth_factor = 1):
        self.name = name
        self.x = x
        self.y = y
        self.population = population
        self.growth_factor = growth_factor

        # Set default starting curve.
        self.demand_curve = Linear(-1,5)

        # Assume to start, each person demands one megabit of bandwidth
        self.demand = population * 1000000

    # Accessor functions
    def GetName(self):
        return self.name

    def GetCoord(self):
        return (self.x,self.y)

    def GetPopulation(self):
        return self.population

    def GetDemand(self):
        return self.demand

    # Update function. This function is called for every city every step.
    def Update(self):
        # A more realistic way to determine growth is needed.
        self.population = self.population + 1
        self.demand = self.population * 1000000
    
