# Defines level 1 

from game import *
from capital import *
from database import *
from networkgraph import *
from city import *
from economic import *

def level1_setup(game_obj):
    # Make a list of cities
    c = []
    c.append(City("Mountain City",200,200,950000,10))
    c.append(City("Oil Town",1400,467,650000,100))
    c.append(City("Zamma Cityn",1800,167,50000,10))
    c.append(City("Bayville",260,530,1050000,10))
    c.append(City("Station Square",930,920,3050000,100))
    c.append(City("Emerald Coast",510,700,50000,10))
    c.append(City("Southern Junction",1530,1420,3050000,100))
    return Economic(c)

