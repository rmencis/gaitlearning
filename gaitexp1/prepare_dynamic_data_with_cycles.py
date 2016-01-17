import csv
import os.path
import os
import random
import data_util
import numpy

def readData(baseDirPath,trial):
    dirPath = os.path.join(baseDirPath,'T' + str(trial).zfill(3))
    metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")
    dataFilePath = os.path.join(dirPath,'mocap-' + str(trial).zfill(3)+".txt")

    metaData = data_util.getMetaData(metaFilePath)

    rows = []
    with open(dataFilePath, 'rb') as f:
        reader = csv.reader(f, delimiter='\t')
        reader.next() # Skin header
        for row in reader:
            rows.append(row)

    return rows,metaData.subject.id

def readCycles(baseDirPath,trial):
    dirPath = os.path.join(baseDirPath,"cycles")
    cyclesFilePath = os.path.join(dirPath,'cycles-' + str(trial).zfill(3)+".csv")

    cycles = []
    with open(cyclesFilePath, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        row = reader.next()
        cycles = [ int(x) for x in row ]

    return cycles

def produceFeatureFile(baseDirPath,gaitDirPath,trial,outputDirPath):
    rows,subjectId = readData(gaitDirPath,trial)
    cycles = readCycles(baseDirPath,trial)
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    rowCount = len(rows)

    maxFeatures = 100
    markers = [112]
    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        for c in range(len(cycles)-1):
            thisCycle = cycles[c]
            nextCycle = cycles[c+1]

            if (thisCycle >= 10000):
                features = []
                for marker in markers:
                    #values = [float(rows[i][marker]) for i in range(thisCycle,nextCycle)]
                    #arr = numpy.array(values)
                    #if (numpy.mean(arr) > 0):
                    for i in range(thisCycle,min(rowCount,thisCycle+maxFeatures)):
                        value = rows[i][marker]
                        if (i >= nextCycle):
                            value = 0
                        features.append(value)
                features.append(subjectId)
                csvWriter.writerow(features)

    return

trainingTrials = [10,11,12,13,16,18,19,20,25,27,32,33,40,41]
testTrials = [9,15,17,21,26,31,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
trainingFileDirPath = os.path.join(baseDirPath,'feature_files_3/train')
testFileDirPath = os.path.join(baseDirPath,'feature_files_3/test')
finalTrainingFilePath = os.path.join(baseDirPath,'feature_files_3/train_data.csv')
finalTestFilePath = os.path.join(baseDirPath,'feature_files_3/test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(baseDirPath,gaitDirPath,trial,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(baseDirPath,gaitDirPath,trial,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)