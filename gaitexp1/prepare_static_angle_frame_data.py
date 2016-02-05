import csv
import os.path
import os
import random
import data_util

def produceFeatureFile(gaitDirPath,angleDirPath,trial,includeSampleWithProbability,outputDirPath):
    metaData = data_util.getMetaDataForTrial(gaitDirPath,trial)

    dirPath = os.path.join(angleDirPath,'T' + str(trial).zfill(3))
    dataFilePath = os.path.join(dirPath,'angles-combined-' + str(trial).zfill(3)+".csv")
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        counter = 0
        with open(dataFilePath, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                features = row[2:16]
                if counter == 0:
                    features.append('Subject')
                    csvWriter.writerow(features)
                else:
                    if random.random() <= includeSampleWithProbability:
                        features.append(metaData.subject.id)
                        csvWriter.writerow(features)
                counter += 1
    return

trainingTrials = [10,11,12,13,16,18,19,20,40,41]
testTrials = [9,15,17,21,42]

baseDirPath = '/Users/rmencis/RUG/Machine_Learning/project'
gaitDirPath = os.path.join(baseDirPath,'perturbed-walking-data-01')
angleDirPath = os.path.join(baseDirPath,'aggregated_angles')
outputDirPath = os.path.join(baseDirPath,'feature_files_4')
trainingFileDirPath = os.path.join(outputDirPath,'train')
testFileDirPath = os.path.join(outputDirPath,'test')
finalTrainingFilePath = os.path.join(outputDirPath,'train_data.csv')
finalTestFilePath = os.path.join(outputDirPath,'test_data.csv')

for trial in trainingTrials:
    print 'Reading training trial',trial
    produceFeatureFile(gaitDirPath,angleDirPath,trial,0.01,trainingFileDirPath)

for trial in testTrials:
    print 'Reading test trial',trial
    produceFeatureFile(gaitDirPath,angleDirPath,trial,0.01,testFileDirPath)

print 'Mergin training files'
data_util.mergeCSVFiles(trainingFileDirPath,finalTrainingFilePath)
print 'Mergin test files'
data_util.mergeCSVFiles(testFileDirPath,finalTestFilePath)
