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

def getMetaDataForTrial(gaitTrialBasePath,trial):
    dirPath = os.path.join(gaitTrialBasePath,'T' + str(trial).zfill(3))
    metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")

    return getMetaData(metaFilePath)


def printTrialData(baseDirPath,fromTrial,toTrial):
    for trial in range(fromTrial,toTrial):
        dirPath = os.path.join(baseDirPath,'T' + str(trial).zfill(3))
        metaFilePath = os.path.join(dirPath,'meta-' + str(trial).zfill(3)+".yml")
        if (os.path.exists(metaFilePath)):
            metaData = getMetaData(metaFilePath)
            #print 'Trial {}, subject {}'.format(metaData.trial.id,metaData.subject.id)
            print metaData.subject.gender

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

