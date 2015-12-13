import tensorflow as tf
import csv
import random

labelCount = 11

def readData(dataFilePath,markerIndex):
    fromIndex = markerIndex*3
    toIndex = (markerIndex*3)+3
    data = []
    labels = []
    header = []
    with open(dataFilePath, 'rb') as f:
        reader = csv.reader(f)
        header = reader.next()[fromIndex:toIndex] # Skip header
        for row in reader:
            dataRow = row[fromIndex:toIndex]
            [float(i) for i in dataRow]
            label = int(row[len(row)-1])
            labelRow = [0] * labelCount
            labelRow[label-1] = 1
            data.append(dataRow)
            labels.append(labelRow)
    return data,labels,header

# Read data
trainDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files/train_data.csv'
testDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files/test_data.csv'

for markerIndex in range(0,47):
    trainData,trainLabels,trainHeaders = readData(trainDataFilePath,markerIndex)
    testData,testLabels,testHeaders = readData(testDataFilePath,markerIndex)

    # Training

    inputUnitCount = len(trainData[0])
    outputUnitCount = labelCount

    sess = tf.InteractiveSession()
    x = tf.placeholder(tf.float32, shape=[None, inputUnitCount])
    y_ = tf.placeholder(tf.float32, shape=[None, outputUnitCount])

    W = tf.Variable(tf.zeros([inputUnitCount,outputUnitCount]))
    b = tf.Variable(tf.zeros([outputUnitCount]))

    sess.run(tf.initialize_all_variables())

    y = tf.nn.softmax(tf.matmul(x,W) + b)
    crossEntropy = -tf.reduce_sum(y_ * tf.log(y))
    trainStep = tf.train.GradientDescentOptimizer(0.01).minimize(crossEntropy)

    batchSize = 100
    trainDataStartIndex = 0
    for i in range(10000):
        if (trainDataStartIndex >= len(trainData)):
            trainDataStartIndex = 0
        trainDataEndIndex = min(trainDataStartIndex+batchSize,len(trainData))
        dataRows = trainData[trainDataStartIndex:trainDataEndIndex]
        labelRows = trainLabels[trainDataStartIndex:trainDataEndIndex]
        trainStep.run(feed_dict={x: dataRows, y_: labelRows})
        trainDataStartIndex = trainDataStartIndex + batchSize

    correctPrediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correctPrediction, "float"))
    trainAccuracy = accuracy.eval(feed_dict={x: trainData, y_: trainLabels})
    testAccuracy = accuracy.eval(feed_dict={x: testData, y_: testLabels})
    print 'Marker {}, training accuracy {}, test accuracy {}'.format(trainHeaders,trainAccuracy,testAccuracy)

    sess.close()