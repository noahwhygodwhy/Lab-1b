import sys
import math
from terrain import Terrain
from heapq import heappush, heappop
from node import Node


xDistance = 10.29
yDistance = 7.55



"""
getNeighbors
args:   orig: the origin node
        tm: the 2d terrainMap of Nodes

purpose:does the indexing to find the 8 horizontal/vertical/diagonal neighbors
        to the origin node

returns:a list of 0 to 8 neighbors
"""
def getNeighbors(orig, tm):
    x = orig.coords[0]
    y = orig.coords[1]

    neighbors = []
    if y > 0:#protects top
        if x > 0:
            neighbors.append(tm[y-1][x-1]) #top left
        neighbors.append(tm[y-1][x]) #top
        if x < (len(tm[0])-1):
            neighbors.append(tm[y-1][x+1]) #top right    
    if x > 0:
        neighbors.append(tm[y][x-1]) #left
    if x < (len(tm[0])-1):
        neighbors.append(tm[y][x+1]) #right
    if y < (len(tm)-1):#protects bot
        if x > 0:
            neighbors.append(tm[y+1][x-1]) #bottom left
        neighbors.append(tm[y+1][x]) #bottom
        if x < (len(tm[0])-1):
            neighbors.append(tm[y+1][x+1]) #bottom right
    
    
    
    return neighbors


"""
toblersDE
args:   d: the distance difference between two points
        e: the elevation difference between two points

purpose:A helper function to trueToblers allowing the input of a distance
        and elevation instead of an angle or ratio

returns:the walking speed between those two points based on Toblers Function
"""
def toblersDE(d, e): 
    if d == 0:
        return 0.71 
    return trueToblers((e/d))


"""
toblersAngle
args: Angle, the angle between a line between the two points and a flat plane

purpose:A helper function to trueToblers allowing the input of a distance
        and elevation instead of an distance/elevation or ratio

returns:the walking speed between those two points based on Toblers Function
"""
def toblersAngle(angle):
    return trueToblers(math.tan(math.radians(angle)+0.05))


"""
toblersDE
args:S the ratio of elevation/distance between the two points

purpose:An implementation of Tobler's function to calculate the walking speed
        on smooth terrain at a certain angle. Speed is returned in meters/second

returns:the walking speed between those two points based on Toblers Function
"""
def trueToblers(S):
    return 6 * pow(math.e, (-3.5*abs(S+0.05)))/3.6

"""
getHCost
args:   orig: the starting Node
        end: the destination Node

purpose:A function to calculate the underestimated cost of traveling
        from orig to end. The calculation is:
        the straight line distance between the two points * 
        the difficulty factor of the easiest terrain *
        the fastest walking speed possible based on Toblers Function

returns:the estimated H cost between orig and end
"""
def getHCost(orig, end): 
    xTravel = abs(orig.coords[0] - end.coords[0]) * xDistance
    yTravel = abs(orig.coords[1] - end.coords[1]) * yDistance
    zTravel = abs(orig.elevation - end.elevation)
    return math.hypot(zTravel, (xTravel + yTravel)) * (Terrain.ROAD.difficulty()) / toblersAngle(-2.86)

"""
getTransitionCost
args:   orig: the starting Node
        dest: the destination Node

purpose:A function to calculate the actual cost of traveling
        from orig to end. The calculation is:
        the straight line distance between the two points * 
        the difficulty factor destination terrain *
        the walking speed based on Toblers Function

returns:the actual transition cost (G) between orig and dest
"""
def getTransitionCost(orig, dest):
    distance = 0
    if orig.coords[0] == dest.coords[0]:
        distance = yDistance
    elif orig.coords[1] == dest.coords[1]:
        distance = xDistance
    else:
        distance = math.hypot(xDistance, yDistance)
    elevation = dest.elevation - orig.elevation
    #print("elevation change is", elevation)
    trueDistance = math.hypot(distance, elevation)
    return trueDistance * dest.terrain.difficulty() / toblersDE(trueDistance, elevation)

"""
starItUp
args:   start: the starting Node
        end: the destination Node
        terrainMap: the 2d array of Nodes making up the map

purpose:Conducts an a* path finding search between the two points to
        find the most efficient path.
        

returns:True if a path is found, false if not
        The path can is then reconstructed by tracing previous nodes
        from the end node to the start. The path itself is not returned.
"""
def starItUp(start, end, terrainMap):


    startNode = terrainMap[start[1]][start[0]]
    endNode = terrainMap[end[1]][end[0]]
    openNodes = [startNode] #starts the heap off
    startNode.f = getHCost(startNode, endNode)
    startNode.g = 0

    while len(openNodes) > 0:
        current = heappop(openNodes)
        if current.coords == end:
            return True
        for neighbor in getNeighbors(current, terrainMap):
            newG = current.g + getTransitionCost(current, neighbor)
            newH = getHCost(neighbor, endNode)
            if newG < neighbor.g:
                neighbor.previous = current.coords
                neighbor.g = newG
                neighbor.h = getHCost(neighbor, endNode)
                neighbor.f = neighbor.g + neighbor.h
                if not neighbor in openNodes:
                    heappush(openNodes, neighbor)       
    return False
    
