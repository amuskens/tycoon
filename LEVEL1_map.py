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
    c.append(City("Edmonton",200,200,950000,10))
    c.append(City("Calgary",230,500,1050000,10))
    return Economic(c)

