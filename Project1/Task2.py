'''
 CSC 527 - Project 1
 Author: Tien Pham
'''

from random import random
import matplotlib.pyplot as plt
import math
import numpy as np
from copy import deepcopy


def Predict(row, weights):
    activation = weights[0]
    for i in range(len(row) - 1):
        activation += weights[i+1] * row[i]
    if activation >= 0.0:
        return 1.0
    else:
        return -1.0

def TrainWeights(dataset, learningRate, nEpoch):
    weights = [0.0 for i in range(len(dataset[0]))]
    MSE_list = []

    #for each epoch, calculate MSE and update the weights of the neural network
    for epoch in range(nEpoch):
        MSE = 0.0
        for row in dataset:
            prediction = Predict(row, weights)
            error = row[-1] - prediction
            MSE += error ** 2
            weights[0] = weights[0] + learningRate * error
            for i in range(len(row) - 1):
                weights[i+1] = weights[i+1] + learningRate * error * row[i]
        MSE = MSE / len(dataset)
        MSE_list.append(MSE)

        # if MSE is equal to 0, break the loop
        if(MSE == 0.0):
            break
    return MSE_list, weights


def DisplayResult(MSE_list, weights, dataset):
    '''
    :param MSE_list: list of mean square error
    :param weights:  weights of the neural network
    :param dataset:  The dataset used to plot
    :return: None
    '''

    #plot MSE in each epoch
    plt.plot(range(1, len(MSE_list) + 1),MSE_list)
    plt.ylabel("MSE")
    plt.xlabel("Number of epochs")
    if (len(MSE_list) <= 10):
        n_epoch = 10
    else:
        n_epoch = len(MSE_list)
    plt.axis([1, n_epoch, 0, max(MSE_list)])
    plt.show()

    #classify the dataset into 2 subsets by label predictions
    label1PredictionFilter = dataset[:,0]*weights[1] + dataset[:,1]*weights[2] >= -weights[0]
    label1PredictionDataset = dataset[label1PredictionFilter]
    label2PredictionFilter = dataset[:,0]*weights[1] + dataset[:,1]*weights[2] < -weights[0]
    label2PredictionDataset = dataset[label2PredictionFilter]

    #plot classification line
    x = np.asarray([-20,35])
    y = -(weights[0] + weights[1]*x)/weights[2]
    plt.plot(x, y, c="g")

    #plot data points
    plt.scatter(label1PredictionDataset[:,0], label1PredictionDataset[:,1], c="r", s=10)
    plt.scatter(label2PredictionDataset[:,0], label2PredictionDataset[:,1], c="b", s=10)
    plt.xlim(-20, 35)
    plt.show()


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


#initialize variables
learningRate = 0.0001
nEpopch = 100

#create a data set
dataset = moon(2000, 0, 10, 6)
dataset = np.asarray(dataset)

#process the dataset
dataset1 = np.resize(deepcopy(dataset[0]), (1, len(dataset[0])))
dataset1 = np.append(dataset1, np.resize(deepcopy(dataset[2]), (1, len(dataset[0]))), axis=0)
dataset1 = np.append(dataset1, np.ones((1, len(dataset1[0])))*-1, axis=0)
dataset1 = dataset1.transpose()

dataset2 = np.resize(deepcopy(dataset[1]), (1, len(dataset[1])))
dataset2 = np.append(dataset2, np.resize(deepcopy(dataset[3]), (1, len(dataset[1]))), axis=0)
dataset2 = np.append(dataset2, np.ones((1, len(dataset2[0]))), axis=0)
dataset2 = dataset2.transpose()

processedDataset = np.append(dataset1, dataset2, axis=0)

#shuffle the data set
np.random.shuffle(processedDataset)

#train the dataset and return Mean square root errors and weights
MSE_list, weights = TrainWeights(processedDataset, learningRate, nEpopch)

#plot the result
DisplayResult(MSE_list, weights, processedDataset)
