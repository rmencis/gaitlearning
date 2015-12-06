import csv
import os.path
import os
import random

class SubjectData:
    def __init__(self):
        self.id = 0
        self.age = 0
        self.mass = 0
        self.gender = ''

class TrialData:
    def __init__(self):
        self.id = None

class MetaData:
    def __init__(self):
        self.subject = SubjectData()
        self.trial = TrialData()

def getMetaData(metaFilePath):
    metaData = MetaData()

    with open(metaFilePath) as f:
        lines = f.readlines()

    section = None
    for line in lines:
        if line.startswith('subject:'):
            section = 'subject'
        elif line.startswith('trial:'):
            section = 'trial'
        if (section == 'subject'):
            if line.strip().startswith('id:'):
                metaData.subject.id =  int(line[line.rfind(' ')+1:])
            if line.strip().startswith('age:'):
                metaData.subject.age =  int(line[line.rfind(' ')+1:])
            if line.strip().startswith('mass:'):
                metaData.subject.mass =  int(line[line.rfind(' ')+1:])
            if line.strip().startswith('gender:'):
                metaData.subject.gender = line[line.rfind(' ')+1:].strip()
        if (section == 'trial'):
            if line.strip().startswith('id:'):
                metaData.trial.id =  int(line[line.rfind(' ')+1:])


    return metaData

def printTrialData(baseDirPath,fromTrial,toTrial):
    for trial in range(fromTrial,toTrial):
        dirPath = os.path.join(baseDirPath,'T' + str(trial).zfill(3))
        metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")
        if (os.path.exists(metaFilePath)):
            metaData = getMetaData(metaFilePath)
            #print 'Trial {}, subject {}'.format(metaData.trial.id,metaData.subject.id)
            print metaData.subject.gender


def produceFeatureFile(baseDirPath,trial,includeSampleWithProbability,outputDirPath):
    dirPath = os.path.join(baseDirPath,'T' + str(trial).zfill(3))
    metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")
    dataFilePath = os.path.join(dirPath,'mocap-' + str(trial).zfill(3)+".txt")
    outputFilePath = os.path.join(outputDirPath,'t' + str(trial).zfill(3) + ".csv")

    metaData = getMetaData(metaFilePath)

    with open(outputFilePath, 'wb') as outputCSVFile:
        csvWriter = csv.writer(outputCSVFile)
        counter = 0
        with open(dataFilePath, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            for row in reader:
                features = row[2:142]
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

def mergeCSVFiles(dirPath,outputFilePath):
    headerRow = None
    rows = []
    for fileName in os.listdir(dirPath):
        if fileName.endswith(".csv"):
            filePath = os.path.join(dirPath,fileName)
            with open(filePath, 'rb') as f:
                reader = csv.reader(f)
                headerRow = reader.next()
                for row in reader:
                    rows.append(row)
    random.shuffle(rows)
    with open(outputFilePath, 'wb') as outputCSVFile:
        writer = csv.writer(outputCSVFile)
        writer.writerow(headerRow)
        for row in rows:
            writer.writerow(row)

trials = [9,10,11,12,13,14,15,16,17,18,19,20,21,25,26,27,31,32,33,40,41,42]

featureFileDirPath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files'
finalFeatureFilePath = '/Users/rmencis/RUG/Machine_Learning/project/final_feature_files/data.csv'

#for trial in trials:
#    print trial
#    produceFeatureFile('/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01',trial,0.01,featureFileDirPath)

mergeCSVFiles(featureFileDirPath,finalFeatureFilePath)

#printTrialData('/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01',1,45)

#print produceFeatureFile('/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01',31,0.01,'/Users/rmencis/RUG/Machine_Learning/project/feature_files')

#print getMetaData('/Users/rmencis/RUG/Machine_Learning/project/perturbed-walking-data-01/T031/meta-031.yml').trial.id

#hello = tf.constant('Hello, TensorFlow!')
#sess = tf.Session()
#print sess.run(hello)

