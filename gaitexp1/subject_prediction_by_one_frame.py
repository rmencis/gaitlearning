import tensorflow as tf
import csv
import random

# Read data
dataFilePath = '/Users/rmencis/RUG/Machine_Learning/project/final_feature_files/data.csv'

labelCount = 11

data = []
labels = []
with open(dataFilePath, 'rb') as f:
    reader = csv.reader(f)
    reader.next() # Skip header
    for row in reader:
        dataRow = row[0:len(row)-2]
        [float(i) for i in dataRow]
        label = int(row[len(row)-1])
        labelRow = [0] * labelCount
        labelRow[label-1] = 1
        data.append(dataRow)
        labels.append(labelRow)

# Split in training and test data

trainingRatio = 0.7
splitIndex = int(len(data) * trainingRatio)
trainingData = data[0:splitIndex]
trainingLabels = labels[0:splitIndex]
testData = data[splitIndex:len(data)]
testLabels = labels[splitIndex:len(labels)]

print len(data)
print len(trainingData)
print len(testData)

# Training

inputUnitCount = len(data[0])
outputUnitCount = labelCount

print inputUnitCount
print outputUnitCount

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
    print i
    trainDataStartIndex = random.randrange(len(trainingData))
    trainDataEndIndex = min(trainDataStartIndex+batchSize,len(trainingData))
    dataRows = trainingData[trainDataStartIndex:trainDataEndIndex]
    labelRows = trainingLabels[trainDataStartIndex:trainDataEndIndex]
    train_step.run(feed_dict={x: dataRows, y_: labelRows})

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
print 'Accuracy {}'.format(accuracy.eval(feed_dict={x: testData, y_: testLabels}))
#print 'Accuracy {}'.format(accuracy.eval(feed_dict={x: testData, y_: trainingLabels[0:len(testLabels)]}))

# Test
#for i in range(len(testData)):
#    dataRow = testData[i]
#    label = testLabels[i]


sess.close()