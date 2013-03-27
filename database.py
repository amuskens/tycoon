import sys
import os.path

# Import all the different types of items.
from capital import Item
from capital import Structure
from capital import Building
from capital import Tower
from capital import Network
from capital import Router
from capital import PointToPoint
from capital import Radio
from capital import Wired

"""
The idea is to load the item specs from the config files into the overall template database.

Not finished implementing all item types.

"""

class CapitalDatabase():
    """
    Tests:


    >>> Data = CapitalDatabase()
    >>> a = Data.GetTower(0)
    >>> a.name
    'Titan T200'
    >>> not Data.Towers == None
    True
    >>> not Data.Radios == None
    True

    """

    def __init__(self):
        # Set the file path to point in the directory.
        file_path = os.path.dirname(__file__)
        if file_path != "":
            os.chdir(file_path)

        # Load in the database dictionaries from files.
        # These dictionaries contain the possible items you can buy for the game.
        self.Towers = self.loadDict("gameconfig/towers.cfg")
        self.Radios = self.loadDict("gameconfig/radios.cfg")
        self.WiredConnections = self.loadDict("gameconfig/wired.cfg")
        self.Routers = self.loadDict("gameconfig/routers.cfg")
        self.Buildings = self.loadDict("gameconfig/buildings.cfg")

    # Load in the contents of a configuration file in order to 
    # build the database of capital.
    def loadDict(self,filename):
        inFile = open(filename,'r')
        returnDict = { }
        id = 0

        for line in inFile:
            line = line.rstrip()
            fields = line.split(",")

            # Allow comments in config file.
            if fields[0] == '#': continue

            tempList = []
            for field in fields:
                tempList.append(field)

            returnDict[id] = tempList
            id = id + 1
                
        return returnDict

    def GetTower(self,id):
        return Tower(self.Towers[id])

    def GetRadio(self,id):
        return Radio(self.Radios[id])

    def GetWired(self,id):
        return WiredConnections(self.WiredConnections[id])

    def GetRouter(self,id):
        return Router(self.Routers[id])

    def GetBuilding(self,id):
        return Building(self.Buildings[id])

if __name__ == "__main__":
    import doctest
    doctest.testmod()
