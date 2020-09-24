import sys
from enum import Enum

"""
An enum class to store information about the different terrain types
Contains the difficulty factor, and the color tuple (r,g,b)
"""
class Terrain(Enum):

    #these are supposed to be how many seconds it takes to traverse 10 meters of that type of land
    OPEN_LAND = 15, (248, 148, 18)
    ROUGH_MEDOW = 45, (255, 192, 0)
    EASY_MOVE_FOREST = 18, (255, 255, 255)
    SLOW_RUN_FOREST = 24, (2, 208, 60)
    WALK_FOREST = 30, (2, 136, 40)
    IMPASSIBLE_VEGITATION = 120, (5, 73, 24)
    WATER = sys.maxsize, (0, 0, 255)
    ROAD = 4, (71, 51, 3)
    TRAIL = 6, (0, 0, 0)
    TRAIL_LEAFY = 10, (168, 107, 0)
    NO_NO_ZONE = sys.maxsize, (205, 0, 101)
    ICE = 20, (165, 242, 243)
    MUD = 25, (145, 108, 20) #depends on the mud, but we'll call it 25
    ERROR = 0, (148, 0, 211)

    
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj.__value__ = args[0]
        obj._rgb_ = args[1]
        return obj

    def difficulty(self):
        return self.__value__

    def __str__(self):
        return self.name
    
    def color(self):
        return self._rgb_