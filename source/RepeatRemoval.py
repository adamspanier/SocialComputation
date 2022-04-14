#!/usr/bin/env python3

def removeRepeats(word):
	newString = ''.join([j for i,j in enumerate(word) if j not in word[:i]])
	print(newString)

removeRepeats("omgggggg")
