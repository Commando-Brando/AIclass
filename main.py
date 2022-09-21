# Add only your imports here - following are the ones that may be enough to finish the assignment
import pandas as pd
import matplotlib.pyplot as plt
from queue import PriorityQueue
import geopy.distance
import numpy as np
from collections import deque
import pickle
import io

# Assume that the data files are in the following folder -- THIS WILL BE USED BY THE TA
basePath = "/content/drive/MyDrive/Colab Notebooks/Artificial Intelligence/Data/"
map = "texas-map.png"

class Node:
    def __init__(self, name, lon, lat):
        self.name = name
        self.lon = lon
        self.lat = lat
        self.path = 0
        self.neighbors = []

    def __str__(self):
        return f'{self.name:<20} {str(self.lon):<8} {str(self.lat):<10} {str(self.path):<7} {self.neighbors}\n'

    def __repr__(self):
        return f'{self.name:<20} {str(self.lon):<8} {str(self.lat):<10} {str(self.path):<7} {self.neighbors}\n'

citiesDF = pd.read_csv('cities.csv', header=None)
distanceDF = pd.read_csv('distances.csv', header=None)
NUM_CITIES = len(citiesDF)

mapX1,mapX2 = 107,93
mapY1,mapY2 = 25,37.5

citiesList = [Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values]
citiesDic = {city[0]:Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values}

# TODO make generate docstring thing here
def createMap(color='red', plotOrder=False, orderList=[]):
    txMap = plt.imread(map)
    fig, ax = plt.subplots()

    def connectpoints(origin:str, destination:str, distance:float):
        x1, x2 = citiesDic[origin].lat, citiesDic[destination].lat
        y1, y2 = citiesDic[origin].lon, citiesDic[destination].lon
        ax.plot([x1,x2],[y1,y2],'b-')
        
    def midpointLabel(origin:str, destination:str, distance:float):
        x1, x2 = citiesDic[origin].lat, citiesDic[destination].lat
        y1, y2 = citiesDic[origin].lon, citiesDic[destination].lon
        # calculate mid point
        x,y = ((x1+x2)/2, (y1+y2)/2)
        ax.text(x,y, str(distance), fontsize=8, color=color)
    
    # TODO make this a function because below was all auto generated
    def orderLabel(origin:str, destination:str, distance:float, order:int):
        x1, x2 = citiesDic[origin].lat, citiesDic[destination].lat
        y1, y2 = citiesDic[origin].lon, citiesDic[destination].lon
        # calculate mid point
        x,y = ((x1+x2)/2, (y1+y2)/2)
        ax.text(x,y, str(order), fontsize=8, color=color)

    ax.imshow(txMap, extent=[mapX1,mapX2,mapY1,mapY2], origin='upper')
    ax.scatter([city.lat for city in citiesList], [city.lon for city in citiesList])
    ax.set_xlim(mapX1, mapX2)
    ax.set_ylim(mapY1, mapY2)
    ax.set(title='Texas', xlabel='Latitude', ylabel='Longitude')

    for i, c in enumerate(citiesList):
        ax.annotate(c.name, (c.lat, c.lon))

    for i in range(len(distanceDF)):
        connectpoints(distanceDF[0][i], distanceDF[1][i], distanceDF[2][i])
        midpointLabel(distanceDF[0][i], distanceDF[1][i], distanceDF[2][i])
        
    #TODO fix this for loop to work with orderLabel Function
    for i in range(len(orderList)):
        orderLabel(origin, destination, distance, order)

createMap()
plt.show()

for i in range(len(distanceDF)):
    citiesDic[distanceDF[0][i]].neighbors.append((distanceDF[1][i], distanceDF[2][i])) # appends neighbors list with a tuple of the neighbor and their distance
    citiesDic[distanceDF[1][i]].neighbors.append((distanceDF[0][i], distanceDF[2][i])) 

def markPathOrder(cityName):
    pass

def bfs(start:Node, goal:int) -> int:
    explored = set()
    pathCost = 0
    citiesExpanded = []
    
    frontier = deque()
    frontier.append(start)
    explored.add(start.name)
    
    while frontier:
        city = frontier.popleft() 
        citiesExpanded.append(city.name)
        
        if len(explored) == goal: # if all cities have been explored return path cost
            citiesExpanded.extend(list(frontier)) # append remaining cities in the queue to our city
            return pathCost, citiesExpanded
        
        for neighbor in city.neighbors: # neighbor is a tuple of the neighbor and the distance
            if neighbor[0] not in explored:
                pathCost += neighbor[1] # add distance to neighbor to path cost
                explored.add(neighbor[0]) # add city to explored set
                frontier.append(citiesDic[neighbor[0]])

def dfs(start:Node, goal:int) -> int:
    explored = set()
    
    frontier = deque()
    frontier.append(start)
    
    while frontier:
        city = frontier.popleft() 
        explored.add(city.name) # add city to explored set
        
        if len(explored) == goal: # if all cities have been explored return path cost
            return city.name # TODO figure out path cost
        
        for neighbor in city.neighbors: # neighbor is a tuple of the neighbor and the distance
            if neighbor[0] not in explored:
                citiesDic[neighbor[0]].path = city.path + neighbor[1] # set path cost of neighbor to path cost of current city + distance to neighbor
                frontier.append(citiesDic[neighbor[0]])

bfsPathCost, bfsCitiesExpanded = bfs(citiesDic['San Antonio'], NUM_CITIES)
# print(bfsPathCost)
# print(bfsCitiesExpanded)
createMap(plotOrder=True, orderList=bfsCitiesExpanded)
plt.show()

# print the sum of all values in the third column in distances data frame
# sum = 0
# for row in distanceDF.values:
#     sum += row[2]
# print(sum)