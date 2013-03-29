""" 
Main Game Starter

"""

import sys
import random
import agentsim
from game import *

arg_debug = 0

# Need to implement steps
def do_init():
    pass

def do_step():
    pass

def main():
    game = Game(title="Telecom Network Tycoon", init_fn=do_init, step_fn=do_step)
    game.start()


if __name__ == "__main__":
    # if we don't have this conditional main body code, then pydoc3 gets
    # really cofused trying to partially run the code to extract out the
    # methods etc.

    # only bring in all the tk stuff when really running
    import agentsim
    main()
