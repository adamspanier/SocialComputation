#!/usr/bin/env python3

import csv
import pandas as pd

def main():
    howToUse()
    fileName = getFileName()
    #fieldNum = getNumStringFields()
    #fieldNums = getFieldNums(fieldNum)
    cleanFile(fileName)
    congrats()

def howToUse():
    print("\n*** Adams Weka Extractor: a Super, Ostentaious, Magnificent Expirement (AWESOME) ***")
    print("\n*** To Use ***\n\n1. Copy this code into the same directory as your dataset .csv")
    print("2. Run the code\n3. When promped, please type the EXACT name of the file, including the extension. e.g. tweets.csv")
    print("6. YES, I KNOW I CAN\'T COUNT! Relax and let the program do its thing! :)\n")
    print("*** Begin User Input ***\n")
    
def getFileName():
    name = input("Please enter the file name: ")
    return name
    
def getNumStringFields():
    fieldNum = int(input("Please enter the number of string fields in the dataset: "))
    return fieldNum
    
def getFieldNums(numStringFields):
    fieldNums = []
    print("Please enter field numbers starting with lowest first. Press ENTER between each field number.")
    for x in range(numStringFields):
        fieldNums.append(int(input("Field num " + str(x+1) + ": ")))
    return fieldNums
    
def cleanFile(fileName):
    newOutName = "CLEAN_" + fileName
    with open(fileName) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
    
        for row in csvReader:
            outputFile = open(newOutName, "a")
            writer = csv.writer(outputFile, escapechar=' ', quoting=csv.QUOTE_NONE)
              
            #strip quotes and single quotes from all
            count = 0
            for field in row:
                tempField = str(row[count])
                tempField = tempField.replace('"','')
                tempField = tempField.replace("'",'')
                tempField = tempField.replace(",",'')
                tempField = tempField.rstrip()
                tempField = tempField.encode("ascii", "ignore").decode()
                row[count] = tempField.replace("\n","")
                count = count + 1
            
            writer.writerow(row)
            outputFile.close()

def congrats():
    print("\n*** Dance Time ***\n")
    print("Your Dataset should be Weka Compatible now!")
    print("")
if __name__ == "__main__":
    main()
