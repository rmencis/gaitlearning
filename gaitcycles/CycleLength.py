# -*- coding: utf-8 -*-
"""
Created on Sun Jan 03 13:09:35 2016

@author: T. van Tuijl
"""
import os.path
from decimal import Decimal
import numpy

def clusterFrames(frameList, offset):
    previousEntry = frameList[0]
    clusterList = []
    cycleCounter = 0
    for entry in frameList:
        if entry[0] - previousEntry[0] > offset:
            clusterList.append([previousEntry[0], previousEntry[1], cycleCounter])
            cycleCounter += 1
        previousEntry = entry
    return(clusterList)

def loadFile(fileName):
    if os.path.isfile(fileName+".txt"):
        loadedFile = open(fileName + ".txt", "r")
        frameList =[]
        for line in loadedFile:
            splitLine = line.split("\t")
            if splitLine[0] != "TimeStamp":
                relevant = [int(splitLine[1]), Decimal(splitLine[112]), Decimal(splitLine[136])]
                frameList.append(relevant)
        loadedFile.close()
        return frameList

def getCycles(frameList, thresHold, offset):        
        relevantList = []
        for entry in frameList:
            diff = abs(entry[1]-entry[2])
            if diff < thresHold:
                relevantList.append([entry[0], diff])
                
         
        del frameList 
        clusters = clusterFrames(relevantList, offset)
        
        
        cycles = []
        previous = relevantList[0]
        for entry in clusters:
            currentCycle = []
            differences = []
                
            for item in relevantList :
                if item[0] <= entry[0] and item[0] > previous[0]:
                    currentCycle.append([item[0], item[1], entry[2]])
                    differences.append(item[1])
                    
            refpoint = min(differences)
            for item in currentCycle:
                if item[1] == refpoint:
                    cycles.append(item[0])
            previous = entry   
        return(cycles)

            
def checkCycles(cycles, sensitivity):
    lengths = []
    for i in range(0,len(cycles)-1):
        currentLength = cycles[i+1]-cycles[i]
        lengths.append(currentLength)
    meanL = numpy.mean(lengths)
    stdevL =  numpy.std(lengths)
    deviations = []
    for i in range(0,len(cycles)-1):
        currentLength = cycles[i+1]-cycles[i]
        if (currentLength-meanL)/stdevL > sensitivity:
            deviations.append(cycles[i])
    return(deviations)
           
                

            

