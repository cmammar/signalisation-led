from json import loads
from copy import deepcopy
from math import sqrt
from time import sleep

class Node():
    def __init__(self, name, localDistance, quality, parent):
        self.name = name
        self.localDistance = localDistance
        self.quality = quality
        self.parent = parent

    def __repr__(self):
        return "%s: Q: %s | parent: %s" % (self.name, self.quality, self.parent)

def fileToList(filename):
    f = open(filename, 'r')
    a = loads(f.read())
    f.close()
    return a

def createShopObjects(shops):
    res = {}
    for shop in shops:
        res[shop.pop('name')] = shop
    return res

def calcDistance(xa, ya, xb, yb):
    return sqrt((xa- xb) **2 + (ya - yb)**2)

def createMatrixLocalDistance(shops, shopsObj):
    res = {}
    points = [shop['name'] for shop in shops]
    for point in points:
        xa = shopsObj[point]['x']
        ya = shopsObj[point]['y']
        inter = {}
        for p in points:
            if p in shopsObj[point]['link']:
                inter[p] = calcDistance(xa, ya, shopsObj[p]['x'], shopsObj[p]['y'])
            else:
                inter[p] = -1
        res[point] = inter
        # print(inter)
    return res

def createDictTotalDistance(shops, shopsObj, destinationPoint):
    res = {}
    points = [shop['name'] for shop in shops]
    xb = shopsObj[destinationPoint]['x']
    yb = shopsObj[destinationPoint]['y']
    for point in points:
        xa = shopsObj[point]['x']
        ya = shopsObj[point]['y']
        res[point] = calcDistance(xa, ya, xb, yb)
    # print(res)
    return res

def printMatrix(matrix):
    for line in matrix:
        print(line)

def isInList(name, my_list):
    for i in range(len(my_list)):
        if my_list[i].name == name:
            return i
    return -1

def extractPath(closeList):
    res = []
    end = closeList.pop()
    while end.parent != None:
        res.append(end.name)
        end = closeList[isInList(end.parent, closeList)]
    res.append(closeList[0].name)
    res.reverse()
    return res

def astar(shopsObj, matrixLocalDistance, matrixTotalDistance, deb, end):
    openList = []
    closeList = [Node(deb, 0, 0, None)]
    actual_node = closeList[0]
    while actual_node.name != end:
        # print("NODE ACTUELLE : "+actual_node.name)
        for link in shopsObj[actual_node.name]['link']:
            if isInList(link, closeList) == -1:
                localDistance = actual_node.localDistance + matrixLocalDistance[actual_node.name][link]
                quality = localDistance + matrixTotalDistance[link]
                index = isInList(link, openList)
                if index != -1:
                    if quality < openList[index].quality:  
                        openList[index] = Node(link, localDistance, quality, actual_node.name)
                else:
                    openList.append(Node(link, localDistance, quality, actual_node.name))
        if len(openList) == 0:
            return []
        openList.sort(key=lambda x: x.quality)
        actual_node = deepcopy(openList[0])
        closeList.append(openList.pop(0))
    return extractPath(closeList)

# récupère l'id de la bande sur laquelle est le point
def findBandeFromPath(shopsObj, bandes, src, dest):
    if shopsObj[src]['x'] == shopsObj[dest]['x']:
        axe = 'y'
        opo = 'x'
    else:
        axe = 'x'
        opo = 'y'
    # print("AXE = "+axe)
    for b in bandes:
        if b['axe'] == axe and shopsObj[src][opo] == b[opo] and (shopsObj[src][axe] >= b['deb'] and shopsObj[src][axe] <= b['end'] and
            shopsObj[dest][axe] >= b['deb'] and shopsObj[dest][axe] <= b['end']):
            return b['id'] 

# récupère quelle led allumer en première et en dernière
# après faire une boucle qui allume du deb a la fin
def getFirstLastLed(shopsObj, bandes, src, dest):
    bandIndex = findBandeFromPath(shopsObj, bandes, src, dest) - 1
    print("id bande = "+str(bandIndex + 1))
    if shopsObj[src]['x'] == shopsObj[dest]['x']:
        axe = 'y'
    else:
        axe = 'x'
    deb = shopsObj[src][axe] - bandes[bandIndex]['deb']
    end = shopsObj[dest][axe] - bandes[bandIndex]['deb']
    return deb, end
    #print(str(deb)+" => "+str(end))

def main():
    deb = 'B'
    end = 'F'
    shops = fileToList('shops.json') # [{'name': 'A', 'type': '...'}, {'name': 'B', ...}, ... ]
    bandes = fileToList('bandes.json')
    shopsObj = createShopObjects(deepcopy(shops)) # {'A': {'type': '...'}, 'B': {'type': '...'}, ... }
    matrixLocalDistance = createMatrixLocalDistance(shops, shopsObj)
    matrixTotalDistance = createDictTotalDistance(shops, shopsObj, end)
    path = astar(shopsObj, matrixLocalDistance, matrixTotalDistance, deb, end)
    getFirstLastLed(shopsObj, bandes, "F", "E")

if __name__ == "__main__":
    main()