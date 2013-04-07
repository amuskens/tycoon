""" 
Main Game Starter

"""

import sys
import random
from game import *
import agentsim

global playinggame

arg_debug = 0

def main():
    global action_stack
    action_stack = []
    global playinggame
    playinggame = Game(title="Telecom Network Tycoon")
    playinggame.start()

if __name__ == "__main__":
    main()
