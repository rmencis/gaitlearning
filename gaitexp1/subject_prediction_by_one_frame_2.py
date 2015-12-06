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
            dataRow = row[0:len(row)-1]
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

trainingData,trainingLabels = readData(trainDataFilePath)
testData,testLabels = readData(testDataFilePath)

# Training

inputUnitCount = len(trainingData[0])
outputUnitCount = labelCount

print 'Training samples:',len(trainingData)
print 'Test samples:',len(testData)
print 'Features:',len(trainingData[0])

sess = tf.InteractiveSession()
x = tf.placeholder(tf.float32, shape=[None, inputUnitCount])
y_ = tf.placeholder(tf.float32, shape=[None, outputUnitCount])

W = tf.Variable(tf.zeros([inputUnitCount,outputUnitCount]))
b = tf.Variable(tf.zeros([outputUnitCount]))

sess.run(tf.initialize_all_variables())

y = tf.nn.softmax(tf.matmul(x,W) + b)
cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

batchSize = 100
for i in range(10000):
    print 'Training batch:',i
    trainDataStartIndex = random.randrange(len(trainingData))
    trainDataEndIndex = min(trainDataStartIndex+batchSize,len(trainingData))
    dataRows = trainingData[trainDataStartIndex:trainDataEndIndex]
    labelRows = trainingLabels[trainDataStartIndex:trainDataEndIndex]
    train_step.run(feed_dict={x: dataRows, y_: labelRows})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print
print 'Accuracy on training data: {}'.format(accuracy.eval(feed_dict={x: trainingData, y_: trainingLabels}))
print 'Accuracy on test data: {}'.format(accuracy.eval(feed_dict={x: testData, y_: testLabels}))
#print 'Accuracy {}'.format(accuracy.eval(feed_dict={x: testData, y_: trainingLabels[0:len(testLabels)]}))

# Test
#for i in range(len(testData)):
#    dataRow = testData[i]
#    label = testLabels[i]


sess.close()