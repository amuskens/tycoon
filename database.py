import sys
from capital import Tower

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
        # Load in the database dictionaries from files.
        self.Towers = self.loadDict("towers.cfg")
        self.Radios = self.loadDict("radios.cfg")
        
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
        a = Tower(self.Towers[id])
        return a

    def GetRadio(id):
        a = Radio(self.Radios[id])
        return a


if __name__ == "__main__":
    import doctest
    doctest.testmod()
