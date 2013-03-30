# Defines level 1 

from game import *
from capital import *
from database import *
from networkgraph import *

def level1_setup(game_obj):
    # Test network, showing a demo of how to use the functions:
    game_obj.gameNetwork.NewNode((480,800),"Anders City",[game_obj.ItemDatabase.GetTower(1)])
    game_obj.gameNetwork.AddEdge("Station Square","Anders City",[game_obj.ItemDatabase.GetRadio(3)])
    game_obj.gameNetwork.AddEdge("Anders City","Station Square",[game_obj.ItemDatabase.GetRadio(3)])
    game_obj.gameNetwork.NewNode((300,810),"IslandVille",[])
    game_obj.gameNetwork.AddEdge("IslandVille","Anders City",[])
    game_obj.gameNetwork.NewNode((800,50),"Oil City",[])
    game_obj.gameNetwork.AddEdge("Station Square","Oil City",[])
    game_obj.gameNetwork.AddEdge("Oil City","Station Square",[game_obj.ItemDatabase.GetRadio(0)])
    game_obj.gameNetwork.AddItemsToNode("Station Square",[game_obj.ItemDatabase.GetTower(0),game_obj.ItemDatabase.GetTower(1)])