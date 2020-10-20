'''
 CSC 527 - Homework 4
 Author: Tien Pham
'''

from random import random
import matplotlib.pyplot as plt
import math
import numpy as np

def calculateCostFunction(x, y, w, Lambda):
    m = x.shape[0]
    epsilon = (1. / (2. * m)) * (np.sum((np.dot(x, w) - y) ** 2.) + Lambda * np.dot(w.T, w))
    return epsilon

def updateWeight(x, y, w, epoch, learningRate, Lambda):
    m = x.shape[0]
    epsilon = np.zeros((epoch, 1))

    for i in range(epoch):
        epsilon[i] = calculateCostFunction(x, y, w, Lambda)
        w = w - (learningRate / m) * (np.dot(x.T, (x.dot(w) - y[:, np.newaxis])) + Lambda * w)

    return w, epsilon

def trainData(x, y, epoch, learningRate, Lambda):

    xn = np.ndarray.copy(x)
    yn = np.ndarray.copy(y)

    #Initial weight w0 = [0, 0, 0]
    w = np.zeros((xn.shape[1] + 1, 1))

    x_mean = np.mean(xn, axis=0)
    x_std = np.std(xn, axis=0)
    xn -= x_mean
    x_std[x_std == 0] = 1
    xn /= x_std

    y_mean = yn.mean(axis=0)
    yn -= y_mean

    xn = np.hstack((np.ones(xn.shape[0])[np.newaxis].T, xn))

    w, epsilon = updateWeight(xn, yn, w, epoch, learningRate, Lambda)

    return w, epsilon


def getDataSet(num_points, distance, radius, width):
    x1, x2, y1, y2 = moon(num_points, distance, radius, width)

    x1 = np.array(x1)
    x2 = np.array(x2)
    x = np.concatenate((x1, x2))
    output1 = np.ones(num_points)

    y1 = np.array(y1)
    y2 = np.array(y2)
    y = np.concatenate((y1, y2))
    output2 = np.zeros((num_points))

    XX = np.vstack([x, y])
    YY = np.concatenate((output1, output2))

    return XX.T, YY

def moon(num_points,distance,radius,width):

    points = num_points

    x1 = [0 for _ in range(points)]
    y1 = [0 for _ in range(points)]
    x2 = [0 for _ in range(points)]
    y2 = [0 for _ in range(points)]

    for i in range(points):
        d = distance
        r = radius
        w = width
        a = random() * math.pi
        x1[i] = math.sqrt(random()) * math.cos(a)*(w/2) + ((-(r+w/2) if(random() < 0.5) else (r+w/2)) * math.cos(a))
        y1[i] = math.sqrt(random()) * math.sin(a)*(w) + (r * math.sin(a)) + d

        a = random() * math.pi + math.pi
        x2[i] = (r+w/2) + math.sqrt(random()) * math.cos(a)*(w/2) + ((-(r+w/2)) if (random() < 0.5) else (r+w/2)) * math.cos(a)
        y2[i] = -(math.sqrt(random()) * math.sin(a)*(-w) + (-r * math.sin(a))) - d
    return ([x1, x2, y1, y2])

def displayDecisionBoundary(w, x):
    '''
    The decision boundary: y = -(w0 + w1x)/w2
    '''
    x = np.linspace(np.amin(x), np.amax(x), 100)
    y = -(w[0] + x * w[1]) / w[2]
    plt.plot(x, y, '--k', label="Decision Boundary")

#initialize variables
learningRate = 0.0001
nEpoch = 100
Lambda = 1
dist = [0, 1, -2, -4]

for d in dist:
    #create a train dataset
    x_train, y_train = getDataSet(1500, d, 10, 6)

    #create a test dataset
    x_test, y_test = getDataSet(2000, d, 10, 6)

    w, epsilon = trainData(x_train, y_train, nEpoch, learningRate, Lambda)

    displayDecisionBoundary(w, x_train)

    for i in range(len(y_test)):
        if x_test[i][1] > (-(w[0] + x_test[i][0] * w[1]) / w[2]):
            plt.scatter(x_test[i][0], x_test[i][1], c="r", s=10)
        else:
            plt.scatter(x_test[i][0], x_test[i][1], c="b", s=10)
    plt.title("Distance = " + str(d))
    plt.show()

    it = np.linspace(0, 100, 100)

    plt.plot(it, epsilon)
    plt.xlabel("Epochs")
    plt.ylabel("Cost")
    plt.title("Distance = " + str(d))
    plt.show()
