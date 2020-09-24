from terrain import Terrain #ignore warning, it's just stupid
from astar import starItUp
from astar import getNeighbors #for the seasonal changes
from node import Node
from queue import *
import sys
from PIL import Image
from datetime import datetime
from math import hypot

possibleSeasons = ("winter", "summer", "fall", "spring")
xDistance = 10.29
yDistance = 7.55
"""
checkpoint
args:   coords, a 2-tuple of (x,y)
        terrainimagePixels, the pixel access of the loaded terrain image

purpose:Puts a 3x3 pixel square marker on the image to mark path endpoints

returns:None
"""
def checkpoint(coords, terrainImagePixels):
    for x in range(coords[0]-1, coords[0]+2):
        for y in range(coords[1]-1, coords[1]+2):
            terrainImagePixels[x, y] = (3, 91, 87)
    terrainImagePixels[coords[0], coords[1]] = (255, 0, 0)

"""
clearMap
args:map: the 2d terrainMap of Nodes

purpose:clears all Nodes of f/g/h/previous values so it can be reused.

returns:None
"""
def clearMap(map):
    for y in map:
        for node in y:
            node.f = sys.maxsize
            node.h = sys.maxsize
            node.g = sys.maxsize
            node.previous = None

"""
watlChecker (Water Adjacent To Land)
args:   node: The node we're checking
        map: the 2d terrainMap of Nodes

purpose:checks if a node is a water node adjacent to a node that isn't water

returns:true if there is an adjacent node that is not water, false if not
"""
def watlChecker(node, terrainMap):
    if node.terrain == Terrain.WATER:
        for n in getNeighbors(node, terrainMap):
            if not n.terrain == Terrain.WATER:
                return True
    return False


"""
tatfChecker (Trail Adjacent To Forest)
args:   node: The node we're checking
        map: the 2d terrainMap of Nodes

purpose:checks if a node is a trail node adjacent to a EASY_MOVE_FOREST node

returns:true if there is an adjacent node that is EASY_MOVE_FOREST,false if not
"""
def tatfChecker(node,terrainMap):
    if node.terrain == Terrain.TRAIL:
        for n in getNeighbors(node, terrainMap):
            if n.terrain == Terrain.EASY_MOVE_FOREST:
                return True
    return False

"""
iceItUp
args:   watl: a list of all nodes in the terrain that are water adjacent to land
        terrainMap: the 2d terrainMap of Nodes
        terrainImagePixels: the pixel access for the loaded terrain image

purpose:conducts a breadth first search from watl nodes. Converts any
        water node within 7 water nodes of a watl node to ice.

returns:None, modifies terrainMap in place
"""
def iceItUp(watl, terrainMap, terrainImagePixels):
    q = Queue()
    for w in watl:
        w.previous = True
        w.terrain = Terrain.ICE
        terrainImagePixels[w.coords] = Terrain.ICE.color()
        w.f = 0     
        q.put(w)
    while not q.empty():
        current = q.get()
        for n in getNeighbors(current, terrainMap):
            if not n.previous == True:
                n.visited = True
                if n.terrain == Terrain.WATER:
                    if current.f < 6:
                        n.terrain = Terrain.ICE
                        terrainImagePixels[n.coords] = Terrain.ICE.color()
                        n.f = current.f+1
                        q.put(n)
            else: #if it's already been visited
                if n.f > current.f+1 and current.f+1 < 6:
                    n.terrain = Terrain.ICE
                    terrainImagePixels[n.coords] = Terrain.ICE.color()
                    n.f = current.f+1
                    q.put(n)

                

    


"""
mudItUp
args:   watl: a list of all nodes in the terrain that are water adjacent to land
        terrainMap: the 2d terrainMap of Nodes
        terrainImagePixels: the pixel access for the loaded terrain image

purpose:conducts a breadth first search from watl nodes. Converts any
        land node within 15 nodes and 1 meter of elevation to any watl node
        to a mud node

returns:None, modifies terrainMap in place
"""
def mudItUp(watl, terrainMap, terrainImagePixels):

    notMuddable = (Terrain.ROAD, Terrain.WATER, Terrain.NO_NO_ZONE)

    q = Queue()
    for w in watl:
        w.previous = True
        w.h = w.elevation #storing water level in the h slot
        w.f = 0
        q.put(w)
    while not q.empty():
        current = q.get()
        for n in getNeighbors(current, terrainMap):
            if not n.previous == True:
                n.visited = True
                if not n.terrain in notMuddable:
                    if current.f < 15 and n.elevation < current.h+1:
                        n.terrain = Terrain.MUD
                        terrainImagePixels[n.coords] = Terrain.MUD.color()
                        n.h = current.h
                        n.f = current.f+1
                        q.put(n)
            else: #if it's already been visited
                if n.f > current.f+1 and current.f+1 < 15 and n.elevation < current.h+1:
                    n.terrain = Terrain.MUD
                    terrainImagePixels[n.coords] = Terrain.MUD.color()
                    n.f = current.f+1
                    q.put(n)


"""
getDistance
args:   n1, a 2 tuple (x,y) of coords
        n2, a 2 tuple (x,y) of coords

purpose:finds the distance between two points on the map based on coords
precondition: this is only used by the path tracer, so it's assumed the 
              two coordinates are neighbors

returns:the distance between the two nodes at these coords
"""
def getDistance(n1, n2):
    if n1[0] == n2[0]:
        return yDistance
    if n2[1] == n2[1]:
        return xDistance
    return hypot(xDistance, yDistance)

"""
mudItUp
args:   [0] lab1.py
        [1] the terrain image
        [2] the elevation file
        [3] the path file
        [4] the season string
        [5] the output image file name used to save the results

purpose:constructs a terrain map out of the terrain image and elevation file
        modifies it according to the season
        then conducts a pathfinding search using a* to find the optimal path
        between the points provided int he path file.

returns:None, the resulting path is displayed as an image when finished
        that image is also saved as the filename provided
"""
def main():

    if(not len(sys.argv) == 6):
        print("\033[1;31mUsage: python lab1.py <terrainImage> <elevationFile> <pathFile> <season> <outputFileName>\033[0m")
        exit(0)

    season = str.lower(sys.argv[4])

    if(not season in possibleSeasons):
        print("\033[1;31mInvalid season, possible seasons are spring, summer, fall, winter\033[0m")
        exit(0)

    terrainImageName =  sys.argv[1]
    elevationFileName = sys.argv[2]
    pathFileName = sys.argv[3]
    outputImageName = sys.argv[5]

    #load in terrain image
    try:
        terrainImage = Image.open(terrainImageName).convert('RGB')
    except Exception as e:
        print("\033[1;31mTerrain file not found, error produced is:\033[0m\n", e)
        exit(0)
    terrainImagePixels = terrainImage.load()
    
    #initalize terrain map
    width, height = terrainImage.size
    terrainMap = [[Node() for x in range(width)] for y in range(height)]

    
    #easy terrain type access based on color tuple(r,g,b)
    colorDictionary = {}
    for x in Terrain:
        colorDictionary[x.color()] = x
    
    try:
        elevationFile = open(elevationFileName)
    except Exception as e:
        print("\033[1;31mElevation file not found, error produced is:\033[0m\n", e)
        exit(0)
        
    #read in elevations and set up Nodes in terrainMap
    try:
        for y in range(height):
            individualElevations = elevationFile.readline().split()
            for x in range(width):
                cNode = terrainMap[y][x]
                cNode.coords = (x, y)
                cNode.elevation = float(individualElevations[x])
                cNode.terrain = colorDictionary[terrainImagePixels[x,y]]
        
    except IndexError as e:
        print("\033[1;31mIf you're seeing this, either I messed up big time, or your provided elevation file is too short in height or width\033[0m\n",e)
        exit(0)

    watl = [] #Water adjacent to land
    elevationFile.close()

    #after map is loaded in, run through it again for seasonal stuff
    for y in range(height):
        for x in range(width):
            cNode = terrainMap[y][x]
            if season == "winter" or season == "spring":
                if watlChecker(cNode, terrainMap):
                    watl.append(cNode)
            if season == "fall":
                if tatfChecker(cNode,terrainMap):
                    cNode.terrain = Terrain.TRAIL_LEAFY
                    terrainImagePixels[cNode.coords] = Terrain.TRAIL_LEAFY.color()

    #if it's spring, apply mud
    if season == "spring":
        mudItUp(watl, terrainMap, terrainImagePixels)
    #if it's winter, apply ice
    if season == "winter":
        iceItUp(watl, terrainMap, terrainImagePixels)


    paths = []    
    with open(pathFileName, 'r') as pathFile:
        for line in pathFile:
            x, y = line.split()
            paths.append((int(x),int(y)))
    #for each pair of paths
    totalDistance = 0
    for i in range(len(paths)-1):
        start = paths[i]
        end = paths[i+1]
        print("working on path between",start,"and",end)
        clearMap(terrainMap) #resets all the f/g/h/previous values
        if starItUp(start, end, terrainMap):#if there's a result
            current = end                   #color in the path
            while not current == start:
                terrainImagePixels[current] = Terrain.ERROR.color()
                totalDistance += getDistance(current, end)
                current = terrainMap[current[1]][current[0]].previous
            terrainImagePixels[start] = Terrain.ERROR.color()
        
        checkpoint(start, terrainImagePixels)#mark the start/end
        checkpoint(end, terrainImagePixels)
        
    print("Total distance:", round(totalDistance, 2), "meters")
    terrainImage.save(outputImageName) #save and show
    terrainImage.show()
    
if __name__ == "__main__":
    main()