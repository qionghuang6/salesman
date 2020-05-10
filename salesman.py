#! /usr/bin/python3

import sys
import csv

def getDataset(name):
    f = open("points.csv", 'r')
    minPath = 0
    xcoords = list()
    ycoords = list()
    bestpath = list()
    for line in f:
        if name in line:
            minPath = float(line.split(',')[1])
        elif (minPath != 0 and len(xcoords) == 0):
            xcoords = line.rstrip().split(',')
        elif(len(xcoords) != 0 and len(ycoords) == 0):
            ycoords = line.rstrip().split(',')
        elif(len(ycoords) != 0 and len(bestpath) == 0):
            bestpath = line.rstrip().split(',')
    f.close()
    return minPath,xcoords,ycoords,bestpath

def main():
    a9 =  getDataset('A9')
    print('A9:')
    for val in a9:
        print(val)    
    
main()