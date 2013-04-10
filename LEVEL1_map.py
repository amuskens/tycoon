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
    c.append(City("Northern Junction",800,223,2950000,100))
    c.append(City("Oil City",1960,467,650000,100))
    c.append(City("Zamma City",1800,167,50000,10))
    c.append(City("Bayville",90,630,32500,10))
    c.append(City("Bayside",150,499,12500,10))
    c.append(City("Station Square",930,920,3050000,100))
    c.append(City("Emerald Coast",510,700,68000,10))
    c.append(City("Southern Junction",1530,1420,3050700,100))
    c.append(City("Midway",1430,620,2830,10))
    c.append(City("Trafelgar",1830,1020,5050700,1700))
    c.append(City("South Town",1430,1220,2030,10))
    c.append(City("Sunny Brooks",1230,1350,12745,10))
    c.append(City("Sunnyside",1230,1076,1745,10))
    c.append(City("Forest Town",1930,1676,81745,10))
    return Economic(c)

