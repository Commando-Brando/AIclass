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

x1,x2 = 107,93
y1,y2 = 25,37.5

citiesList = [Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values]
citiesDic = {city[0]:Node(city[0], city[1], float(str(city[2]).split('-')[1])) for city in citiesDF.values}

# maxLon, minLon = max([city.lon for city in cities]), min([city.lon for city in cities])
# maxLat,minLat = max([city.lat for city in cities]), min([city.lat for city in cities])

txMap = plt.imread(map)
fig, ax = plt.subplots()

def connectpoints(city1, city2, distance):
    x1, x2 = citiesDic[city1].lat, citiesDic[city2].lat
    y1, y2 = citiesDic[city1].lon, citiesDic[city2].lon
    ax.plot([x1,x2],[y1,y2],'b-')
    
def midpointLabel(city1, city2, distance):
    x1, x2 = citiesDic[city1].lat, citiesDic[city2].lat
    y1, y2 = citiesDic[city1].lon, citiesDic[city2].lon
    # calculate mid point
    x,y = ((x1+x2)/2, (y1+y2)/2)
    ax.text(x,y, str(distance), fontsize=8, color='red')

ax.imshow(txMap, extent=[x1,x2,y1,y2], origin='upper')
ax.scatter([city.lat for city in citiesList], [city.lon for city in citiesList])
ax.set_xlim(x1, x2)
ax.set_ylim(y1, y2)
plt.xlabel('Latitude')
plt.ylabel('Longitude')

for i, c in enumerate(citiesList):
    ax.annotate(c.name, (c.lat, c.lon))

for i in range(len(distanceDF)):
    connectpoints(distanceDF[0][i], distanceDF[1][i], distanceDF[2][i])
    midpointLabel(distanceDF[0][i], distanceDF[1][i], distanceDF[2][i])
plt.show()