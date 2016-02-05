import csv
import os.path
import os
import random
import data_util

def produceFeatureFile(gaitDirPath,angleDirPath,trial,outputDirPath):
    metaData = data_util.getMetaDataForTrial(gaitDirPath,trial)

    dirPath = os.path.join(angleDirPath,'T' + str(trial).zfill(3))
    dataFilePath = os.path.join(dirPath,'angles-combined-' + str(trial).zfill(3)+".csv")
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    # RTOERHEERLEK=2
    # RHEERLEKRGTRO=3
    # RLEKRGTRORASIS=4
    # RGTRORASISNAVE=5
    # LTOELHEELLEK=6
    # LHEELLEKLGTRO=7
    # LLEKLGTROLASIS=8
    # LGTROLASISNAVE=9
    # LLWLLEELDELT=10
    # LLEELDELTLSHO=11
    # LDELTLSHOSTRN=12
    # RLWRLEERDELT=13
    # RLEERDELTRSHO=14
    # RDELTRSHOSTRN=15

    angleIndexes = [9,11]

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        with open(dataFilePath, 'rb') as f:
            reader = csv.reader(f)
            reader.next() # Skip header
            prevCycle = -1
            featureDic = {}
            for row in reader:
                cycle = row[16]
                if (cycle != prevCycle):
                    writeRow(csvWriter,featureDic,metaData.subject.id)
                    featureDic = {}
                    prevCycle = cycle
                for angleIndex in angleIndexes:
                    angle = row[angleIndex]
                    if (featureDic.has_key(angleIndex) == False):
                        featureDic[angleIndex] = []
                    featureDic[angleIndex].append(angle)
            writeRow(csvWriter,featureDic,metaData.subject.id)

    return

def writeRow(csvWriter,featureDic,subject):
    allFeatures = []
    if (len(featureDic) > 0):
        for angleIndex in range(16):
            if (featureDic.has_key(angleIndex)):
                features = featureDic[angleIndex]
                maxFeatures = 1
                for i in range(maxFeatures):
                    if (i < len(features)):
                        allFeatures.append(features[i])
                    else:
                        allFeatures.append(0)
        allFeatures.append(subject)
        csvWriter.writerow(allFeatures)

trainingTrials = [10,11,12,13,16,18,19,20,25,27,32,33,40,41]
testTrials = [9,15,17,21,26,31,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
angleDirPath = os.path.join(baseDirPath,'aggregated_angles')
outputDirPath = os.path.join(baseDirPath,'feature_files_5')
trainingFileDirPath = os.path.join(outputDirPath,'train')
testFileDirPath = os.path.join(outputDirPath,'test')
finalTrainingFilePath = os.path.join(outputDirPath,'train_data.csv')
finalTestFilePath = os.path.join(outputDirPath,'test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(gaitDirPath,angleDirPath,trial,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(gaitDirPath,angleDirPath,trial,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)
