""" 
Main Game Starter

"""

import sys
import random
from game import *

arg_debug = 0

def main():
    game = Game(title="Telecom Network Tycoon")
    game.start()


if __name__ == "__main__":
    # if we don't have this conditional main body code, then pydoc3 gets
    # really cofused trying to partially run the code to extract out the
    # methods etc.

    # only bring in all the tk stuff when really running
    import agentsim
    main()