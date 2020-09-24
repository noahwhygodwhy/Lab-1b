from terrain import Terrain
import sys


"""
A class to represent the pixels in the map in a way that makes using a*
to find a path easier.
"""
class Node:
    def __init__(self):
        self.coords = (0,0)
        self.previous = None
        self.g = sys.maxsize
        self.h = sys.maxsize
        self.f = 0
        self.elevation = 0
        self.terrain = Terrain.ERROR
    
    #sorts by fcost
    def __lt__(self, other):
        if type(other) == Node:
            return self.f < other.f
        return False
    
    #nodes are the same node if they're in the same location
    def __eq__(self, other):
        if type(other) == Node:
            if self.coords == other.coords:
                return True
        return False