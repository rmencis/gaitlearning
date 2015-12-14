import csv
import os.path
import os
import random
import data_util

def produceFeatureFile(baseDirPath,trial,includeSampleWithProbability,outputDirPath):
    dirPath = os.path.join(baseDirPath,'T' + str(trial).zfill(3))
    metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")
    dataFilePath = os.path.join(dirPath,'mocap-' + str(trial).zfill(3)+".txt")
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    metaData = data_util.getMetaData(metaFilePath)

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        counter = 0
        with open(dataFilePath, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                features = row[2:143]
                if counter == 0:
                    features.append('Subject')
                    csvWriter.writerow(features)
                else:
                    if random.random() <= includeSampleWithProbability:
                        features.append(metaData.subject.id)
                        csvWriter.writerow(features)
                #print features
                counter += 1
    return

trainingTrials = [10,11,12,13,15,16,18,19,20,25,27,32,33,40,41]
testTrials = [9,14,17,21,26,31,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
trainingFileDirPath = os.path.join(baseDirPath,'feature_files/train')
testFileDirPath = os.path.join(baseDirPath,'feature_files/test')
finalTrainingFilePath = os.path.join(baseDirPath,'feature_files/train_data.csv')
finalTestFilePath = os.path.join(baseDirPath,'feature_files/test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(gaitDirPath,trial,0.01,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(gaitDirPath,trial,0.01,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)
