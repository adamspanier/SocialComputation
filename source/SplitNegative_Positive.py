#!/usr/bin/env python3

import csv

def main():
	iterateCsv()
	
def iterateCsv():
	filename = 'LexicalAnalysis_DataSet.csv'
	posFile = 'positiveSentimentGroup.csv'
	negFile = 'negativeSentimentGroup.csv'
	neuFile = 'neutralSentimentGroup.csv'
	
	with open(filename, 'r') as csvFile:
		reader = csv.reader(csvFile)
		for row in reader:
			if(row[18] == 'Positive'):
				writeToFile(posFile, row)
			if(row[18] == 'Negative'):
				writeToFile(negFile, row)
			if(row[18] == 'Neutral'):
				writeToFile(neuFile, row)
			
def writeToFile(inFile, row):
	with open(inFile, 'a') as inputFile:
		writer = csv.writer(inputFile)
		writer.writerow(row)
		inputFile.close()

if __name__ == "__main__":
    main()
