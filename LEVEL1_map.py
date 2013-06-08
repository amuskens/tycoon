# Defines level 1 

from game import *
from capital import *
from database import *
from networkgraph import *
from city import *
from economic import *

def level1_setup():
    # Make a list of cities
    c = []
    c.append(City("Mountain City",1500,200,950000,10))
    c.append(City("Oil City",3960,467,1050000,100))
    c.append(City("South Town",1430,1220,2030,100))
    c.append(City("Sunny Brooks",1030,1350,12745,10))
    c.append(City("Sunnyside",1530,400,1745,10))
    c.append(City("Forest Town",1930,1676,81745,10)) 
    c.append(City("Station Square",2500,3000,1817451,10))      
            
    bg_image = 'images/terrain.gif'
    w = 4200
    h = 4200
    
    return Economic(c),bg_image,w,h

