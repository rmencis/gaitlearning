# NN with hidden layer

import tensorflow as tf
import csv
import random
import math

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
            #dataRow = row[40*3:(40*3)+3]
            dataRow = row[0:len(row)-1]
            [float(i) for i in dataRow]
            label = int(row[len(row)-1])
            labelRow = [0] * labelCount
            labelRow[label-1] = 1
            data.append(dataRow)
            labels.append(labelRow)
    return data,labels

# Read data
trainDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files_4/train_data.csv'
testDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files_4/test_data.csv'

trainData, trainLabels = readData(trainDataFilePath)
testData,testLabels = readData(testDataFilePath)

inputUnitCount = len(trainData[0])
hiddenUnitCount = 10
outputUnitCount = labelCount

minValueInput = -1/math.sqrt(inputUnitCount)
maxValueInput = 1/math.sqrt(inputUnitCount)
minValueHidden = -1/math.sqrt(hiddenUnitCount)
maxValueHidden = 1/math.sqrt(hiddenUnitCount)

print 'Training samples:',len(trainData)
print 'Test samples:',len(testData)
print 'Features:',len(trainData[0])

x = tf.placeholder(tf.float32, [None, inputUnitCount]) # Input data
W1 = tf.Variable(tf.random_uniform([inputUnitCount, hiddenUnitCount],minval=minValueInput,maxval=maxValueInput))
b1 = tf.Variable(tf.random_uniform([hiddenUnitCount],minval=minValueInput,maxval=maxValueInput))

y1 = tf.tanh(tf.matmul(x, W1) + b1)

W2 = tf.Variable(tf.random_uniform([hiddenUnitCount, outputUnitCount],minval=minValueHidden,maxval=maxValueHidden))
b2 = tf.Variable(tf.random_uniform([outputUnitCount],minval=minValueHidden,maxval=maxValueHidden))

y = tf.nn.softmax(tf.matmul(y1, W2) + b2)

y_ = tf.placeholder(tf.float32, [None, outputUnitCount])

crossEntropy = -tf.reduce_sum(y_ * tf.log(y))

globalStep = tf.Variable(0, trainable=False)
starterLearningRate = 0.001
learningRate = tf.maximum(tf.train.exponential_decay(starterLearningRate, globalStep, 100, 0.995, staircase=True),0.00001)
optimizer = tf.train.GradientDescentOptimizer(learningRate)
trainStep = optimizer.minimize(crossEntropy, global_step=globalStep)

init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)

batchSize = 100
trainDataStartIndex = 0

for i in range(1000000):
    if (trainDataStartIndex >= len(trainData)):
        trainDataStartIndex = 0
    trainDataEndIndex = min(trainDataStartIndex+batchSize,len(trainData))
    #trainDataStartIndex = random.randrange(len(trainData))
    #trainDataEndIndex = min(trainDataStartIndex + batchSize, len(trainData))

    dataRows = trainData[trainDataStartIndex:trainDataEndIndex]
    labelRows = trainLabels[trainDataStartIndex:trainDataEndIndex]
    sess.run(trainStep, feed_dict={x: dataRows, y_: labelRows})
    trainDataStartIndex = trainDataStartIndex + batchSize

    if (i % 100 == 99):
        correctPrediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, "float"))
        print '{}. Training : {}, Test: {}, Loss: {}, Learning rate: {}'.format(i, sess.run(accuracy, feed_dict={x: trainData, y_: trainLabels}),
            sess.run(accuracy, feed_dict={x: testData, y_: testLabels}),
            sess.run(crossEntropy, feed_dict={x: trainData, y_: trainLabels}),
            sess.run(learningRate))



sess.close()