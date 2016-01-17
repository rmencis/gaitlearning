import tensorflow as tf
import csv
import random

labelCount = 11

def readData(dataFilePath):
    data = []
    labels = []
    with open(dataFilePath, 'rb') as f:
        reader = csv.reader(f)
        reader.next() # Skip header
        for row in reader:
            #dataRow = row[0:21]
            dataRow = row[0:len(row)-1]
            [float(i) for i in dataRow]
            label = int(row[len(row)-1])
            labelRow = [0] * labelCount
            labelRow[label-1] = 1
            data.append(dataRow)
            labels.append(labelRow)
    return data,labels

# Read data
trainDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files_3/train_data.csv'
testDataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/feature_files_3/test_data.csv'

trainData, trainLabels = readData(trainDataFilePath)
testData,testLabels = readData(testDataFilePath)

# Training

inputUnitCount = len(trainData[0])
outputUnitCount = labelCount

print 'Training samples:',len(trainData)
print 'Test samples:',len(testData)
print 'Features:',len(trainData[0])

sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None, inputUnitCount])
y_ = tf.placeholder(tf.float32, shape=[None, outputUnitCount])

W = tf.Variable(tf.random_uniform([inputUnitCount,outputUnitCount],minval=-1,maxval=1))
b = tf.Variable(tf.random_uniform([outputUnitCount],minval=-1,maxval=1))

sess.run(tf.initialize_all_variables())

y = tf.nn.softmax(tf.matmul(x,W) + b)
crossEntropy = -tf.reduce_sum(y_ * tf.log(y))
trainStep = tf.train.GradientDescentOptimizer(0.01).minimize(crossEntropy)

batchSize = 100
for i in range(100000):
    trainDataStartIndex = random.randrange(len(trainData)-batchSize)
    trainDataEndIndex = trainDataStartIndex + batchSize
    dataRows = trainData[trainDataStartIndex:trainDataEndIndex]
    labelRows = trainLabels[trainDataStartIndex:trainDataEndIndex]
    trainStep.run(feed_dict={x: dataRows, y_: labelRows})
    if (i % 100 == 0):
        correctPrediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
        accuracy = tf.reduce_mean(tf.cast(correctPrediction, "float"))
        print '{}. Training accuracy: {}, Test accuracy: {}, Cross-entropy loss: {}'.format(i, sess.run(accuracy, feed_dict={x: trainData, y_: trainLabels}),
                                                   sess.run(accuracy, feed_dict={x: testData, y_: testLabels}),
                                                             sess.run(crossEntropy, feed_dict={x: trainData, y_: trainLabels}))
        #with open("/Users/rmencis/RUG/Machine_Learning/project/weights.csv", "wb") as f:
        #    writer = csv.writer(f)
        #    writer.writerows(sess.run(W))

sess.close()