# This class instantiates city objects

import random
import math

from curves import *
import curves

class City():

    # Initialize a new city
    def __init__(self,name,x,y,population=1000,growth_factor = 1):
        self.name = name
        self.x = x
        self.y = y
        self.population = population
        self.growth_factor = growth_factor
        self.highest_price = 10
        # Rate is per bit / s
        self.rate = 1

        self.insupply = 0
        self.outsupply = 0

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

    def SetRate(self,num):
        self.rate = float(num)
    
    def SetSupply(self,num):
        (num1, num2) = num
        self.insupply = num1
        self.outsupply = num2

    def GetSupply(self):
        return (self.insupply,self.outsupply)
    

    # Update function. This function is called for every city every step.
    def Update(self,turn,multiplier,vshift):
        # A more realistic way to determine growth is needed.
        # Update population only once a week.
        if turn % 168 == 0:
            self.population = self.population + 0.5 * self.growth_factor

        dm = (0.5 - random.random()) / 1000 * multiplier
        db = (0.5 - random.random()) / 100 + vshift
        self.demand_curve.m = self.demand_curve.m + dm
        self.demand_curve.b =  self.highest_price + db

    # Calculate the price and quantity, given supply
    # and the rate per Mbps. Return Revenue
    def Revenue(self):
        revenue = 0
        iprice = 0
        iquantity = 0
        
        # Find intersections between the price and the quantity
        int_p = lines_intersect(self.demand_curve,
                                       Linear(0,self.rate))
        
        # For incoming quantitiy supplied:
        int_iqs = line_intersect_vline(self.demand_curve,
                                              self.insupply)

        # If the intersection for quantity is further left,
        # there is a shortage. There is lost revenue
        if int_iqs[0] <= int_p[0]:
            iprice = int_p[1]
            iquantity = int_iqs[0]
            
        # Otherwise, you are charging more, and thus receiving economic rent.
        else:
            iprice = int_p[1]
            iquantity = int_p[0]

        revenue = iquantity * iprice
        

        # Now deal with outgoing
        oprice = 0
        oquantity = 0
        
        # For outgoing quantitiy supplied:
        int_oqs = line_intersect_vline(self.demand_curve,
                                              self.outsupply)

        # If the intersection for quantity is further left,
        # there is a shortage
        if int_oqs[0] <= int_p[0]:
            oprice = int_p[1]
            oquantity = int_oqs[0]
            
        # Otherwise, you are charging more, and thus receiving economic rent.
        else:
            oprice = int_p[1]
            oquantity = int_p[0]
        
        # Debug
        print('Supplies:')
        print(self.insupply)
        print(self.ooutsupply)
        print('Revenue for ' + self.GetName())
        print(iquantity)
        print('$ %0.2f' % iprice)
        print(oquantity)
        print('$ %0.2f' % oprice)

        revenue = iquantity * iprice + oquantity * oprice
        print(revenue)
        return revenue
                                     
    
