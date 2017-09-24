#!/usr/bin/env python3
""" 
::Authors::
Lucas Carpenter
Joey Brown

::Date::
September 22, 2017

::Module Description::
This module handles operations related to training and testing a dataset
using the PatternClassification class. 
"""


def normalize(data):
    """ Create a list of normalized data based off of min/max values and a dataset"""
    #lets make sure everything in the array is a float..
    for i in range(0, len(data)):
        data[i] = list(map(float, data[i]))
    #rotate the array for easy access to min/max
    rotatedArray = list(zip(*data[::-1]))
    #loop through each feature, find the min/max of that feature line, normalize the data on that line, repeat
    for i in range(2, len(rotatedArray)):
        minVal = min(rotatedArray[i])
        maxVal = max(rotatedArray[i])
        #traverse through each sample in list, i is the feature, j is the sample
        for j in range(0, len(rotatedArray[i])):
            #be careful if max or min equal each other, then we are dividing by 0
            if(maxVal-minVal != 0):
                data[j][i] = (data[j][i]-minVal)/(maxVal-minVal)
    return data

def findCentroidData(data, nClasses, nFeatures):
    """ Calculate some sums of all averages for our centroids, we'll remove the test case one later """
    #create our centroidData list (format: [classID][Feat/Samples][if Feat: feat#])
    centroidData = [[[0 for i in range(0, nFeatures)], 0] for i in range(0, nClasses)]
    
    #traverse through each element, summing up the total for each feature and # of samples
    for i in range(0, len(data)):
        #increment # of samples for that class
        centroidData[int(data[i][1])][1] += 1
        #traverse through each feature, adding to the appropriate centroidData piece
        for j in range(2, len(data[i])):
            centroidData[int(data[i][1])][0][j-2] += data[i][j]
    return centroidData

def findPrediction(sample, centroidData):
    """ Calculates centroids for each class type and finds euclidian dist between test case and centroid
        returns a predicted class
    """
    shortestDist = -1
    prediction = None
    #traverse through each feature in our test list and subtract from class's feature data
    for i in range(2, len(sample)):
        centroidData[int(sample[1])][0][i-2] -= sample[i]
    #subtract 1 from total # of samples in the class
    centroidData[int(sample[1])][1] -= 1
    #calculate the average of a centroid, compare to shortestDist and return the class # of shortest distance
    for i in range(0, len(centroidData)):
        if(centroidData[i][1] != 0):
            cavg = [(centroidData[i][0][j]/centroidData[i][1]) for j in range(0, len(centroidData[i][0]))]
            dist = 0
            for j in range(0, len(cavg)):
                dist += (sample[j+2] - cavg[j])**2
            if(dist < shortestDist or shortestDist == -1):
                shortestDist = dist
                prediction = i
    #add back the feature data and increment # of samples in class so we have the original data back
    for i in range(2, len(sample)):
        centroidData[int(sample[1])][0][i-2] += sample[i]
    centroidData[int(sample[1])][1] += 1
        
    return prediction
    
class PatternClassifier:
    """
		The PatternClassifier class holds all information and functions relevant
        to finding a sample's predicted class based on test data given. The class
        stores the test data, the number of classes to compare to, the number of
        features of each sample and the already predicted test cases 
	"""
    title = ""          #the title of our database
    nClasses = 0        #the number of class types
    cNames = []         #the names of the class types (used for output)
    nFeatures = 0       #the number of features
    fNames = []         #the names of the features (used for output)
    nSamples = 0        #the number of samples to train/test on
    SAMPLEDATA = []     #a list of all the sample data including both training/testing data
    centroidData = []   #a list of class information used to calculate the centroid
    correct = []        #a list of sums of correct predictions (format: [[correct, attempted]...])
    predicted = []      #the compiled list of predictions (format: [sampleID, actualClass, predictedClass])

    def __init__(self, title = "", nClasses = 0, cNames = [], nFeatures = 0, fNames = [], nSamples = 0, sampleData = []):
        """ Initialize variables of the class to defaults/set values """
        self.title = title
        self.nClasses = nClasses
        self.cNames = cNames
        self.nFeatures = nFeatures
        self.fNames = fNames
        self.nSamples = nSamples
        self.SAMPLEDATA = normalize(sampleData)
        for i in range(0, self.nClasses):
            self.correct.append([0, 0])
        self.correct.append([0, 0])
        self.centroidData = findCentroidData(self.SAMPLEDATA, self.nClasses, self.nFeatures)

    def setTitle(self, name):
        """ Modify the database title"""
        self.title = name

    def setClasses(self, classNames):
        """ Modify the name/number of class types in the database """
        self.cNames = list(classNames)
        self.nClasses = len(classNames)

    def setFeatures(self, feats):
        """ Modify the feature names and # of features to train upon """
        self.fNames = list(feats)
        self.nFeatures = len(feats)
    
    def setSampleData(self, data):
        """ Modify the data to be trained upon """
        self.SAMPLEDATA = normalize(data)
        self.nSamples = len(data)
        self.centroidData = findCentroidData(self.SAMPLEDATA, self.nClasses, self.nFeatures)

    def train(self, i):
        """ Train our class and test our sample to predict the classtype"""
        prediction = int(findPrediction(self.SAMPLEDATA[i], self.centroidData))
        
        #append our prediction to the prediction list and if we were correct, increment the correct counter
        self.predicted.append([int(self.SAMPLEDATA[i][0]), int(self.SAMPLEDATA[i][1]), prediction])
        self.correct[int(self.SAMPLEDATA[i][1])][1] += 1
        if int(self.SAMPLEDATA[i][1]) == prediction:
            self.correct[prediction][0] += 1
            self.correct[self.nClasses][0] += 1

    def __str__(self):
        """ Convert information from class into an outputable format with all information """
        outstr = str(self.title + "\n")
        outstr = outstr + "MDC parameters: nclasses = " + str(self.nClasses) + ", nfeatures  = " + str(self.nFeatures) + \
        ", nsamples = " + str(self.nSamples) + "\n"
        for i in range(0, self.nClasses):
            outstr = outstr + "class " + str(i) + " (" + self.cNames[i] + "): "
            if self.correct[i][1] == 0:
                outstr = outstr + "-% accuracy (no training/sample data)\n"
            else:
                outstr = outstr + str(f'{self.correct[i][0]/self.correct[i][1]*100:.1f}') +"% accuracy\n"
        outstr = outstr + "overall: " + str(self.nSamples) + " samples, " +  str(f'{self.correct[self.nClasses][0]/self.nSamples*100:.1f}') + "% accuracy\n"
        return str(outstr)
