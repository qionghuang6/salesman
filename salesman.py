#! /usr/bin/python3

import sys
import random

class Dataset:
    def __init__(self, data):
        self.minPath = data[0]
        self.coords = list()
        for i in range(0,len(data[1])):
            self.coords.append([int(data[1][i]), int(data[2][i])])
        self.bestpath = list(map(intify,data[3]))

    def myPrint(self):
        print(self.minPath)
        print(self.bestpath)
        print(self.coords)
         
class Path:
    def __init__(self, coords, order):
        self.coords = coords
        self.order = order
        self.len = 0
        self.fitness = 0
        for i in range(0, len(order) - 1):
            #print("dist ", coords[order[i]], coords[order[i+1]])
            self.len += distance(coords[order[i]],coords[order[i+1]])
        self.len += distance(coords[order[len(order)-1]], coords[order[0]])
        self.fitness = 1.0/self.len
def intify(num):
    return int(num)

def distance(pt1, pt2):
    x1, y1, x2, y2= pt1[0], pt1[1], pt2[0], pt2[1]
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def getDataset(name):
    f = open("points.csv", 'r')
    minPath = 0
    xcoords = list()
    ycoords = list()
    bestpath = list()
    for line in f:
        if (name in line and minPath == 0):
            minPath = float(line.split(',')[1])
        elif (minPath != 0 and len(xcoords) == 0):
            xcoords = line.rstrip().split(',')
        elif(len(xcoords) != 0 and len(ycoords) == 0):
            ycoords = line.rstrip().split(',')
        elif(len(ycoords) != 0 and len(bestpath) == 0):
            bestpath = line.rstrip().split(',')
    f.close()
    return [minPath,xcoords,ycoords,bestpath]

def mate(path1, path2):
    num = random.randint(0,len(path1.order)-1)
    sectionlen = random.randint(1,len(path1.order)-1)
    neworder = list()
    #print("num", num, "sectionlen", sectionlen)
    v = 0
    while(v < len(path1.order)):
        neworder.append(-1)
        v += 1
    for i in range(num,num+sectionlen):
        neworder[i % len(neworder)] = path1.order[i % len(neworder)]
    nextindex = (num + sectionlen) %  len(neworder)
    p2index = (num + sectionlen) %  len(neworder)
    while(-1 in neworder):
        if(path2.order[p2index] not in neworder):
            neworder[nextindex] = path2.order[p2index]
            nextindex = ((nextindex + 1) % len(neworder))
        p2index = ((p2index + 1) % len(neworder))
    return Path(path1.coords, neworder)

def getFit(path):
    return path.fitness

def main():
    setname = 'A9-2'
    population = 100
    generations = 100
    myDataset = Dataset(getDataset(setname))
    paths = list()
    #Set up population
    i = 0
    while (i < population):
        newOrder = myDataset.bestpath[:]
        random.shuffle(newOrder)
        paths.append(Path(myDataset.coords,newOrder))
        i += 1
    # print(paths[0].order)
    # print(paths[1].order)
    # print(mate(paths[0],paths[1]).order)
    j = 0
    while (j < generations):
        weights = list()
        newPaths = list()
        for myPath in paths:
            weights.append(myPath.fitness)
        k = 0
        while(k < len(paths)):
            choice1 = random.choices(paths,weights)[0]
            choice2 = random.choices(paths,weights)[0]
            newPaths.append(mate(choice1, choice2))
            k += 1
        paths = newPaths
        j += 1
    paths.sort(reverse = True, key = getFit)
    print("Calculated Path Length:", round(paths[0].len,3), "Best Path Length:", myDataset.minPath)

    writefile = open("results.csv", 'w')
    writestring = setname + "\n"
    writestring += ",".join(list(map(lambda a : str(a), paths[0].order)))
    writefile.write(writestring)
    writefile.close()

main()