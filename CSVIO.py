#!/usr/bin/env python3
'''
::Authors::
Lucas Carpenter
Joey Brown

::Date::
September 22, 2017

::Module Description::
Module to extract the data within a .csv file and separate it by data details, 
labels, and measurements/raw data.
'''

import csv
import sys


def readDataCSV(filename):
	'''
		Receives a filename to open as a filename.csv. Then returns a 
			list containing the contents of the .csv file.
	'''
	try: 
		csvFile = open(filename, "r") #open filename in "read" mode
		csvReader = csv.reader(csvFile)
		data = []
		for record in csvReader:
			record = [item.strip() for item in record]
			data.append(record)
		csvFile.close()
		return data
	except FileNotFoundError as f:
		print("File not found.")
		sys.exit(1)
	except Exception as e:
		print("An unknown error occured")
		print(e.message())
		sys.exit(1)
# -----------------------------------------------------------------------------

def displayData(data):
	'''
		Prints all of the contents of a dataset.
	'''
	for i in data:
		print(i[0])
		print()
# -----------------------------------------------------------------------------

def getDetails(data):
	'''
		Returns a list containing the details of the dataset within the .csv file.
	'''
	return data[0]
# -----------------------------------------------------------------------------

def getLabels(data):
	'''
		Returns a list of labels for the measurements of the dataset.
	'''
	return data[1]
# -----------------------------------------------------------------------------

def getData(data):
	'''
		Returns just the raw data from the dataset by ignoring the labels
		and the class names.
	'''
	return data[2:]
# -----------------------------------------------------------------------------

def writeToFile(filename, pc):
	'''
		Gets a .csv file and a list of tests. Then writes the results
		of the test to a .cv file with the same name as the .csv.
	'''
	try:
		# pc.predicted to get 
		filename = filename.split(".csv")
		outfile = open(filename[0]+".cv", "w")
		
		# Prints default output from PC class
		print( pc, file = outfile )
		
		print("Sample,Class,Predicted", file = outfile )
		for test in pc.predicted:
			print(str(test[0]) + "," + str(test[1]) + "," + str(test[2]), sep='', end='', file = outfile)
			if test[1] != test[2]:
				print("*", file = outfile)
			else:
				print(" ", file = outfile)
		outfile.close()
		print("Test results written to " +filename[0]+ ".cv")
	except FileNotFoundError as f:
		print("File not found.")
		sys.exit(1)
