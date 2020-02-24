from json import loads
from copy import deepcopy
from math import sqrt

def getShopList(filename):
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
        print(inter)
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
    print(res)
    return res

def printMatrix(matrix):
    for line in matrix:
        print(line)


def astar(shopsObj, matrixLocalDistance, matrixTotalDistance, deb, end):
    openList = []
    closeList = []


def main():
    deb = 'A'
    end = 'G'
    shops = getShopList('shops.json') # [{'name': 'A', 'type': '...'}, {'name': 'B', ...}, ... ]
    shopsObj = createShopObjects(deepcopy(shops)) # {'A': {'type': '...'}, 'B': {'type': '...'}, ... }
    matrixLocalDistance = createMatrixLocalDistance(shops, shopsObj)
    matrixTotalDistance = createDictTotalDistance(shops, shopsObj, 'G')
    astar(shopsObj, matrixLocalDistance, matrixTotalDistance, deb, end)

if __name__ == "__main__":
    main()