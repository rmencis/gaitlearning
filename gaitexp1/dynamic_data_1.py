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

def produceFeatureFile(baseDirPath,trial,probability,outputDirPath):
    rows,subjectId = readData(baseDirPath,trial)
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    rowCount = len(rows)
    stepSize = 1 # Take every STEP_SIZE frame
    stepCount = 500 # Take total STEP_COUNT frames
    windowSize = stepSize * stepCount
    cols = [122]

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)

        for i in range(rowCount-windowSize):
            if random.random() <= probability:
                features = []
                for col in cols:
                    j = i
                    values = []
                    for step in range(stepCount):
                        value = float(rows[j][col])
                        values.append(value)
                        j = j + stepSize
                    arr = numpy.array(values)
                    features.append(numpy.mean(arr))
                    features.append(numpy.median(arr))
                    features.append(numpy.min(arr))
                    features.append(numpy.max(arr))
                    features.append(numpy.std(arr))

                    #[features.append(value) for value in values]
                features.append(subjectId)
                csvWriter.writerow(features)
    return

trainingTrials = [10,11,12,13,16,18,19,20,25,27,32,33,40,41]
testTrials = [9,14,17,21,26,31,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
trainingFileDirPath = os.path.join(baseDirPath,'feature_files_2/train')
testFileDirPath = os.path.join(baseDirPath,'feature_files_2/test')
finalTrainingFilePath = os.path.join(baseDirPath,'feature_files_2/train_data.csv')
finalTestFilePath = os.path.join(baseDirPath,'feature_files_2/test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(gaitDirPath,trial,0.05,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(gaitDirPath,trial,0.05,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)
