from queue import PriorityQueue as pq
from collections import deque
from haversine import haversine, Unit
from math import radians, cos, sin, asin, sqrt
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import great_circle
import numpy as np
import io
import random
import pprint as pp

# Assume that the data files are in the following folder -- THIS WILL BE USED BY THE TA
basePath = "/content/drive/MyDrive/Colab Notebooks/Artificial Intelligence/Data/"
map = "texas-map.png"

# * PANDAS DATAFRAMES *
citiesDF = pd.read_csv('cities.csv', header=None)
distanceDF = pd.read_csv('distances.csv', header=None)

# * CONSTANTS *
NUM_CITIES = len(citiesDF)
COLORS_LIST = ["red", "blue", "orange", "green", "purple", "brown", "black"]

class Node:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.path = 0
        self.neighbors = []

    def __str__(self):
        return f'{self.name:<20} {str(self.lon):<8} {str(self.lat):<10} {str(self.path):<7} {self.neighbors}\n'

    def __repr__(self):
        return f'{self.name:<20} {str(self.lon):<8} {str(self.lat):<10} {str(self.path):<7} {self.neighbors}\n'

class PriorityQueue(pq):
    def __init__(self):
        super().__init__()

    def __str__(self):
        output = ""
        for item in self.queue:
            output += str(item) + "\n"
        return output

mapX1,mapX2 = 106.75,93.5
mapY1,mapY2 = 25.87,36.5

citiesList = [Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values]
citiesDic = {city[0]:Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values}

def drawEdgeDistance(origin:str, destination:str, distance:float, ax, color:str):
        x1, x2 = citiesDic[origin].lat, citiesDic[destination].lat
        y1, y2 = citiesDic[origin].lon, citiesDic[destination].lon
        ax.plot([x1,x2],[y1,y2],'-',color=color)

def midpointLabel(origin:str, destination:str, labelText:str, ax, color:str):
    x1, x2 = citiesDic[origin].lat, citiesDic[destination].lat
    y1, y2 = citiesDic[origin].lon, citiesDic[destination].lon
    x,y = ((x1+x2)/2, (y1+y2)/2) # calculate mid point
    ax.text(x,y, labelText, fontsize=7, color=color)

def drawPathEdge(ax, orderList):
        for i, cityName in enumerate(orderList):
            x,y = citiesDic[cityName].lat, citiesDic[cityName].lon
            ax.text(x,y, i, fontsize=7, color=color)

# * MAP FACTORY *
def mapFactory(color='red', plotCityNames=False, drawEdges=False, plotOrder=False, orderList=[]):
    txMap = plt.imread(map)
    fig, ax = plt.subplots()

    fig.set_size_inches(15,10)
    ax.imshow(txMap, extent=[mapX1,mapX2,mapY1,mapY2], origin='upper')
    ax.scatter([city.lat for city in citiesList], [city.lon for city in citiesList])
    ax.set_xlim(mapX1, mapX2)
    ax.set_ylim(mapY1, mapY2)
    ax.set(title='Texas', xlabel='Latitude', ylabel='Longitude')

    if plotCityNames:
        for i, c in enumerate(citiesList):
            ax.annotate(c.name, (c.lat, c.lon), fontsize=9)
    if drawEdges:
        for i in range(len(distanceDF)):
            drawEdgeDistance(distanceDF[0][i], distanceDF[1][i], distanceDF[2][i], ax, "blue")
            midpointLabel(distanceDF[0][i], distanceDF[1][i], str(distanceDF[2][i]), ax, "red")
    
    return ax

# ! Need to fix mapFactory with new lat/lon
mapFactory(plotCityNames=True, drawEdges=True)
plt.show()

for i in range(len(distanceDF)):
    citiesDic[distanceDF[0][i]].neighbors.append((distanceDF[1][i], distanceDF[2][i])) # appends neighbors list with a tuple of the neighbor and their distance
    citiesDic[distanceDF[1][i]].neighbors.append((distanceDF[0][i], distanceDF[2][i])) 

# * Breadth First Search *
def bfs(start:Node, ax) -> (int, list):
    explored = set() 
    pathCost, expansionOrder = 0, 0 # pathCost tracks the overall total path cost and expansionOrder expansion order of the nodes
    citiesExpanded = [] # creates list of the path sequence
    
    frontier = deque() # FIFO queue
    frontier.append(start)
    explored.add(start.name)
    
    while frontier:
        city = frontier.popleft() 
        citiesExpanded.append(city.name)
        
        for i, neighbor in enumerate(city.neighbors): # neighbor is a tuple of the neighbor and the distance
            if neighbor[0] not in explored:
                expansionOrder += 1
                neighName, neighDistance = neighbor[0], neighbor[1]
                drawEdgeDistance(city.name, neighName, expansionOrder, ax, COLORS_LIST[random.randrange(len(COLORS_LIST))])
                midpointLabel(city.name, neighName, str(expansionOrder), ax, "black")
                pathCost += neighDistance # add distance to neighbor to path cost
                explored.add(neighName) # add city to explored set
                frontier.append(citiesDic[neighName])
    
    return (pathCost, citiesExpanded)

# ax = mapFactory(plotCityNames=True)
# bfsPathCost, bfsCitiesExpanded = bfs(citiesDic['San Antonio'], ax=ax)
# print(f"Part-2 BFS\nTotal Distance Travelled = {bfsPathCost}\nPath:")
# for i, cityName in enumerate(bfsCitiesExpanded):
#     print(f'{i}. {cityName}')
# plt.show()

# * Depth First Search *
def dfs(start:Node, ax) -> int:
    explored, frontier, citiesExpanded = set(), [(start,0, start.name)], [] # explored is out visited set, frontier is our LIFO stack, citiesExpanded is our path list
    pathCost, expansionOrder = 0,0 # pathCost tracks the overall total path cost & expansionOrder expansion order of the nodes
    
    while frontier: # goal is met once the stack is empty meaning we have pursued every possible path
        city,cost,origin = frontier.pop() # cost is the value of the edge from the previous city to the current city
        
        if city.name not in explored:
            citiesExpanded.append(city.name)
            pathCost += cost
            explored.add(city.name)
            drawEdgeDistance(city.name, origin, expansionOrder, ax, COLORS_LIST[random.randrange(len(COLORS_LIST))])
            midpointLabel(city.name, origin, str(expansionOrder), ax, "black")
            expansionOrder += 1
            
            for neighbor in city.neighbors: # neighbor is a tuple of the neighbor and the distance
                if neighbor[0] not in explored:
                    neighName, neighDistance = neighbor[0], neighbor[1]
                    frontier.append((citiesDic[neighName], neighDistance, city.name))
    
    return (pathCost, citiesExpanded)

# ax = mapFactory(plotCityNames=True)
# dfsPathCost, dfsCitiesExpanded = dfs(citiesDic['San Antonio'], ax=ax)
# print(f"Part-2 DFS\nTotal Distance Travelled = {dfsPathCost}\nPath:")
# for i, cityName in enumerate(dfsCitiesExpanded):
#     print(f'{i}. {cityName}')
# plt.show()

def distance_d(LaA, LaB, LoA, LoB):
    # The function "radians" is found in the math module, It's also used to convert radians to degrees.  
    LoA = radians(LoA)  
    LoB = radians(LoB)  
    LaA= radians(LaA)  
    LaB = radians(LaB) 
    # The "Haversine formula" is used.
    D_Lo = LoB - LoA 
    D_La = LaB - LaA 
    P = sin(D_La / 2)**2 + cos(LaA) * cos(LaB) * sin(D_Lo / 2)**2  
    
    Q = 2 * asin(sqrt(P))   
        # The earth's radius in kilometers.
    R_km = 6371  
    # Then we'll compute the outcome.
    return(Q * R_km)

def generateHaversineList(goal:Node) -> dict:
    haversineDic = {}
    for city in citiesList:
        # haversineDic[city.name] = haversine((city.lat, city.lon), (goal.lat, goal.lon), unit=Unit.MILES)
        # print(f'{city.name}: {city.lat} {city.lon}')
        # print(f'{goal.name}: {goal.lat} {goal.lon}')
        haversineDic[city.name] = great_circle((city.lat, city.lon), (goal.lat, goal.lon)).miles
        
    return haversineDic    

# * Greedy Best First Search *
def greedyBFS(start:Node, goal:str, haversineDic:dict, ax) -> (int, list):
    citiesExpanded, currNode = [], start # explored is out visited set, citiesExpanded is our path list
    pathCost, expansionOrder = 0, 1 # pathCost tracks the overall total path cost & expansionOrder expansion order of the nodes
    frontier = PriorityQueue() # priority queue to store node information in a tuple of (haversine, name, pathCostFromOrigin)
    
    while True:
        
        if currNode.name == goal:
            citiesExpanded.append(currNode.name)
            return (pathCost, citiesExpanded)
                
        for neighbor in currNode.neighbors: # neighbor is a tuple of the neighbor and the distance
            frontier.put((haversineDic[neighbor[0]], neighbor[0], neighbor[1])) # put the neighbor in the priority queue with the distance to the goal as the priority
        
        closestNeighbor = frontier.get() # get the closest neighbor
        pathCost += closestNeighbor[2] # add the distance to the neighbor to the path cost
        citiesExpanded.append(currNode.name)
        drawEdgeDistance(currNode.name, closestNeighbor[1], expansionOrder, ax, COLORS_LIST[random.randrange(len(COLORS_LIST))])
        midpointLabel(currNode.name, closestNeighbor[1], str(expansionOrder), ax, "black")
        expansionOrder += 1
        currNode = citiesDic[closestNeighbor[1]] # set the current node to the closest neighbor


ax = mapFactory(plotCityNames=True)
distancesFromCollegeStation = generateHaversineList(citiesDic['College Station'])
gbfsPathCost, gbfsCitiesExpanded = greedyBFS(citiesDic['San Antonio'], 'College Station', distancesFromCollegeStation, ax)
print(f"Part-2 GBFS\nTotal Distance Travelled = {gbfsPathCost}\nPath:")
for i, cityName in enumerate(gbfsCitiesExpanded):
    print(f'{i}. {cityName}')
plt.show()

# * A* Search *
def aStar(start:Node, goal:str, haversineDic:dict, ax) -> (int, list):
    # always pop names of nodes into the frontier
    # g(n) is the cost of the path from the start node to n
    # h(n) is the distance from n to the goal
    
    frontier = PriorityQueue() # priority queue which stores information of nodes in the following tuple (f(n), name, totalpathCost, expansionOrderList)
    frontier.put((0, start.name, 0, [start.name])) # put the start node in the priority queue with the distance to the goal as the priority
    nodesVisited = []
    i = 0
    
    while True: 
        # print(f'{i} ---------------- {frontier}')
        currCity = frontier.get() # get the node with the lowest f(n) value
        nodesVisited.append(currCity[1])
        
        if currCity[1] == goal: # if the node is the goal node, return the path cost and the path
            # print(frontier)
            return (currCity[2], currCity[3], nodesVisited)
        
        for neighbor in citiesDic[currCity[1]].neighbors: # neighbor is a tuple of the neighbor and the distance
            fn = haversineDic[neighbor[0]] + currCity[2] + neighbor[1] # f(n) = g(n) + h(n)
            expandedOrder = currCity[3].copy()
            expandedOrder.append(neighbor[0])
            frontier.put((fn, neighbor[0], neighbor[1] + currCity[2], expandedOrder)) # put the neighbor in the priority queue with the distance to the goal as the priority
        
    return (currCity[2], currCity[3], nodesVisited)

# ! the last 3 cities in nodes visited are not in the right order figure it out
# ax = mapFactory(plotCityNames=True)
# aStarPathCost, aStarCitiesExpanded, nodesVisited = aStar(citiesDic['San Antonio'], 'College Station', distancesFromCollegeStation, ax)
# print(f"Part-3 A*\nNodes Visited -\n{nodesVisited}\nTotal Distance Travelled = {aStarPathCost}\nPath:")
# print(aStarCitiesExpanded)


# print the sum of all values in the third column in distances data frame
# sum = 0
# for row in distanceDF.values:
#     sum += row[2]
# print(sum)


# * References *
# Haversine Formula: https://www.movable-type.co.uk/scripts/latlong.html & https://pypi.org/project/haversine/