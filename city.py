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
        # Rate is $ per bit / s
        self.down_rate = 5.786666667 * math.pow(10,-3)
        self.up_rate = 5.5555 * math.pow(10,-5)

        self.insupply = 0
        self.outsupply = 0

        # Set default starting curve.
        """
        Rationale:

        Assume the average family of 4 has a 6 Mbit/s downlink and
        a 250 kbit/s uplink

        It costs on average $25/mo for this kind of plan
         
        This means every hour, you pay $ 0.03472 for internet

        This means $ 5.786666667 * 10^-9 per bit/s downlink, and
        $ 1.388888889* 10^-7 per bit/s uplink

        So, assuming 50 % of the population has a scheme like this.
        population * 0.5 / 4 * 6 Mbit /s is the quantity downlink
        population * 0.5 / 4 * 250 Kbit/s is the quantity uplink

        To find a second point ont the demand curve, consider 40% of 
        the other families of 4 want 25 Mbit/s internet, which costs $40 per
        month

        $40 / 30 days / 24 hours / 25 Mbit/s = $2.222* 10^-9 per bit/s downlink
        $40 / 30 / 24 / 1 Mbit/s = $5.5555*10^-8 per bit/s uplink

        Quantity is 
        population * 0.4 / 4 * 40 Mbit/s downlink
        population * 0.4 / 4 * 1 Mbit/s uplink

        Using these two points, we can calculate the demand curves

        

        """
        # Use the points from above
        # Downlink
        pt1 = (population * 0.5 / 4 * 6,5, 786666667 * math.pow(10,-6))
        pt2 = (population * 0.4 / 4 * 40, 2.2222222 * math.pow(10,-6))

        m = (pt2[1]-pt1[1]) / (pt2[0] - pt1[0])
        b = pt2[1] - m * pt2[0]

        self.idemand_curve = Linear(m,b)

        # Uplink
        pt1 = (population * 0.5 / 4 * 0.250, 1.3888888897 * math.pow(10,-4))
        pt2 = (population * 0.4 / 4 * 1, 5.5555 * math.pow(10,-5))

        m = (pt2[1]-pt1[1]) / (pt2[0] - pt1[0])
        b = pt2[1] - m * pt2[0]

        self.odemand_curve = Linear(m,b)

        self.idemand_curve.print()
        self.odemand_curve.print()

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
        """
        dm = (0.5 - random.random()) / 1000000 * multiplier
        db = (0.5 - random.random()) / 1000000 + vshift
        self.idemand_curve.m = self.idemand_curve.m + dm
        self.idemand_curve.b =  self.idemand_curve.b + db

        dm = (0.5 - random.random()) / 1000000 * multiplier
        db = (0.5 - random.random()) / 1000000 + vshift
        self.odemand_curve.m = self.odemand_curve.m + dm
        self.odemand_curve.b =  self.odemand_curve.b + db
        """
    # Calculate the price and quantity, given supply
    # and the rate per Mbps. Return Revenue
    def Revenue(self):
        revenue = 0
        iprice = 0
        iquantity = 0
        
        # Incoming
        # Find intersections between the price and the quantity
        int_p = lines_intersect(self.idemand_curve,
                                       Linear(0,self.down_rate))
        
        # For incoming quantitiy supplied:
        int_iqs = line_intersect_vline(self.idemand_curve,
                                              self.insupply / 1000000)

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

        int_p = lines_intersect(self.odemand_curve,
                                       Linear(0,self.up_rate))
        
        # For outgoing quantitiy supplied:
        int_oqs = line_intersect_vline(self.odemand_curve,
                                              self.outsupply / 1000000)

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
        print(self.outsupply)
        print('Revenue for ' + self.GetName())
        print(iquantity)
        print('$ %0.2f' % iprice)
        print(oquantity)
        print('$ %0.2f' % oprice)
        

        revenue = iquantity * iprice + oquantity * oprice
        return revenue
                                     
    
