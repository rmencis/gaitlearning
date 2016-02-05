import csv
import os.path
import os
import random
import data_util
import numpy

def produceFeatureFile(gaitDirPath,distDirPath,trial,outputDirPath):
    metaData = data_util.getMetaDataForTrial(gaitDirPath,trial)

    dirPath = os.path.join(distDirPath,'T' + str(trial).zfill(3))
    dataFilePath = os.path.join(dirPath,'dists-combined-' + str(trial).zfill(3)+".csv")
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    distIndexes = [15,17]

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        with open(dataFilePath, 'rb') as f:
            reader = csv.reader(f)
            reader.next() # Skip header
            prevCycle = -1
            featureDic = {}
            for row in reader:
                cycle = row[20]
                if (cycle != prevCycle):
                    writeRow(csvWriter,featureDic,metaData.subject.id)
                    featureDic = {}
                    prevCycle = cycle
                for distIndex in distIndexes:
                    dist = float(row[distIndex])
                    if (featureDic.has_key(distIndex) == False):
                        featureDic[distIndex] = []
                    featureDic[distIndex].append(dist)
            writeRow(csvWriter,featureDic,metaData.subject.id)

    return

def writeRow(csvWriter,featureDic,subject):
    allFeatures = []
    if (len(featureDic) > 0):
        for distIndex in range(20):
            if (featureDic.has_key(distIndex)):
                features = featureDic[distIndex]
                arr = numpy.array(features)
                allFeatures.append(numpy.mean(arr))
                #allFeatures.append(numpy.median(arr))
                #allFeatures.append(numpy.std(arr))
                #allFeatures.append(numpy.min(arr))
                #allFeatures.append(numpy.max(arr))
                #allFeatures.append(min(len(features) * 0.01,3))
        allFeatures.append(subject)
        csvWriter.writerow(allFeatures)

trainingTrials = [10,11,12,13,16,18,19,20,25,27,32,33,40,41]
testTrials = [9,15,17,21,26,31,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
distDirPath = os.path.join(baseDirPath,'aggregated_physical_distances')
outputDirPath = os.path.join(baseDirPath,'feature_files_8')
trainingFileDirPath = os.path.join(outputDirPath,'train')
testFileDirPath = os.path.join(outputDirPath,'test')
finalTrainingFilePath = os.path.join(outputDirPath,'train_data.csv')
finalTestFilePath = os.path.join(outputDirPath,'test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(gaitDirPath,distDirPath,trial,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(gaitDirPath,distDirPath,trial,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)
