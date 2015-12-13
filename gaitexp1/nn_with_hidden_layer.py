# NN with hidden layer

import tensorflow as tf
import csv
import random

labelCount = 11

def weight_variable(shape):
  #initial = tf.truncated_normal(shape, stddev=0.1)
  initial = tf.random_normal(shape)
  return tf.Variable(initial)

def bias_variable(shape):
  #initial = tf.constant(0.1, shape=shape)
  initial = tf.random_normal(shape)#
  return tf.Variable(initial)

def readData(dataFilePath):
    data = []
    labels = []
    with open(dataFilePath, 'rb') as f:
        reader = csv.reader(f)
        reader.next() # Skip header
        for row in reader:
            dataRow = row[40*3:(40*3)+3]
            #dataRow = row[0:len(row)-1]
            [float(i) for i in dataRow]
            label = int(row[len(row)-1])
            labelRow = [0] * labelCount
            labelRow[label-1] = 1
            data.append(dataRow)
            labels.append(labelRow)
    return data,labels

# Read data
trainDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files/train_data.csv'
testDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files/test_data.csv'

trainData, trainLabels = readData(trainDataFilePath)
testData,testLabels = readData(testDataFilePath)

inputUnitCount = len(trainData[0])
hiddenUnitCount = 20
outputUnitCount = labelCount

print 'Training samples:',len(trainData)
print 'Test samples:',len(testData)
print 'Features:',len(trainData[0])

x = tf.placeholder(tf.float32, [None, inputUnitCount]) # Input data
W1 = weight_variable([inputUnitCount, hiddenUnitCount])
b1 = bias_variable([hiddenUnitCount])

y1 = tf.sigmoid(tf.matmul(x, W1) + b1)

W2 = weight_variable([hiddenUnitCount, outputUnitCount])
b2 = bias_variable([outputUnitCount])

y = tf.nn.softmax(tf.matmul(y1, W2) + b2)

y_ = tf.placeholder(tf.float32, [None, outputUnitCount])

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

crossEntropy = -tf.reduce_sum(y_ * tf.log(y))
trainStep = tf.train.GradientDescentOptimizer(0.001).minimize(crossEntropy)

batchSize = 100
trainDataStartIndex = 0

for i in range(100000):
    if (trainDataStartIndex >= len(trainData)):
        trainDataStartIndex = 0
    trainDataEndIndex = min(trainDataStartIndex+batchSize,len(trainData))
    dataRows = trainData[trainDataStartIndex:trainDataEndIndex]
    labelRows = trainLabels[trainDataStartIndex:trainDataEndIndex]
    sess.run(trainStep, feed_dict={x: dataRows, y_: labelRows})
    trainDataStartIndex = trainDataStartIndex + batchSize

    if (i % 100 == 99):
        correctPrediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, "float"))
        print '{}. Training : {}, Test: {}, Loss: {}'.format(i, sess.run(accuracy, feed_dict={x: trainData, y_: trainLabels}),
                                                   sess.run(accuracy, feed_dict={x: testData, y_: testLabels}),
                                                             sess.run(crossEntropy, feed_dict={x: trainData, y_: trainLabels}))



sess.close()