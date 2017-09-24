#!/usr/bin/env python3
""" 
::Authors::
Lucas Carpenter
Joey Brown

::Date::
September 22, 2017

::Module Description::
Pattern Classification using Minimum Distance Classification
This module reads in a CSV file and groups each class into a 
list of features mapped in a N-dimensional plane. Once all data
has been read in to 'train' the program the final entry will be entered
and the closest distance to the centroid of an already known class will
be used as the new entry's class type.
The CSV file format must follow a pattern similar to below
TITLE, #=CLASSNAME1, #=CLASSNAME2, ..., #=CLASSNAMEX
SAMPLE, CLASS, FEATURE1, FEATURE2, ..., FEATUREX
DATA1, DATA2, ...
"""
import sys
import CSVIO
import training

def main():
    """
    Reads in the CSV file from the command line args and maps features
    of the data to a N-dimensional plane, then tests the accuracy of a
    minimum distance classification algorithm on the data.
    """
    #find sys args and handle appropriately
    argv = sys.argv
    if(len(argv) != 2):
        print("Invalid number of input strings.")
        print("Usage: python mdc.py [inputfile]")
    else:
        #run the IO script, expect out a list of lists, etc..
        data = CSVIO.readDataCSV(argv[1])
        #create a list of classNames from the data, trim/convert as necessary
        classNames = data[0][1:]
        try:
            while(True):
                classNames.remove('')
        except ValueError:
            pass
        try:
            classNames = [item.split('=')[1] for item in classNames]
        except IndexError as ie:
            print("I've failed you Dr. Weiss...")
        #declare/init our class with proper values
        pc = training.PatternClassifier(data[0][0], len(classNames), classNames, len(data[1][2:]), \
        data[1][2:], len(data[2:]), data[2:])
        #run the training data with leaving out i for our test on each sample
        for i in range(0, pc.nSamples):
            pc.train(i)
        #output to console/file
        print(pc)
        CSVIO.writeToFile(argv[1], pc)
            
if __name__ == "__main__": 
    '''This function runs when the module is run from the command line'''
    main()