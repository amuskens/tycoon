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
    c.append(City("Edmonton",3504,6200,1000000,10))  
    c.append(City("Calgary",3602,7702,1100000,10))  
    c.append(City("Lethbridge",4002,8102,100000,10))  
    c.append(City("Drumheller",3702,7+42,8000,10))  
    c.append(City("Red Deer",3530,6900,30000,10))  
    c.append(City("Camrose",3600,6450,10000,10)) 
    c.append(City("Stettler",3700,6550,5000,1)) 
    c.append(City("Fort McMurray",4806,3008,150000,1000))    
    c.append(City("Grande Prairie",1400,5210,80000,10))    
    
    bg_image = []
    bg_image.append('images/levels/alberta20.gif')
    bg_image.append('images/levels/alberta50.gif')
    bg_image.append('images/levels/alberta80.gif')
    bg_image.append('images/levels/alberta.gif')
    
    w = 6000
    h = 10828
    
    return Economic(c),bg_image,w,h

