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
        self.highest_price = 5

        # Set default starting curve.
        self.demand_curve = Linear(0.8 * population / (-self.highest_price),
                                   self.highest_price)

    # Accessor functions
    def GetName(self):
        return self.name

    def GetCoord(self):
        return (self.x,self.y)

    def GetPopulation(self):
        return self.population

    def GetDemand(self):
        return self.demand_curve

    # Update function. This function is called for every city every step.
    def Update(self,turn):
        # A more realistic way to determine growth is needed.
        # Update population only once a week.
        if turn % 168 == 0:
            self.population = self.population + 0.5 * self.growth_factor

        dm = (0.5 - random.random()) / 1000)
        db = (0.5 - random.random()) / 100)
        self.demand_curve.m = self.demand_curve.m + dm
        self.demand_curve.b =  self.highest_price + db
    
