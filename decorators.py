#! /env/bin python

import time

def file_decorator(functionName):
	"""
	change the function's parameters from file indicators to file names
	"""
	def newFunction(inFileName, outFileName, *args):
		inFile = open(inFileName, 'r')
		outFile = open(outFileName, 'w')
		returnValue = functionName(inFile, outFile, *args)
		outFile.close()
		inFile.close()
		return returnValue
	return newFunction

def runtime_decorator(functionName):
	"""
	change the function to print the time for running
	"""
	def newFunction(*args):
		start = time.time()
		returnValue = functionName(*args)
		end = time.time()
		duration = end - start
		print "The running time of the function is %f\n" % duration
		return returnValue
	return newFunction

def file_operation_extension_decorator(functionName):
	"""
	extend the line-of-string-oriented processing to the file-oriented 
	"""
	def newFunction(inFile, outFile, *args):
		inputLineCounter = 0
		outputLineCounter = 0
		
		while True:
			line = inFile.readline()
			if not line: break
			inputLineCounter += 1
			outputLine = functionName(line, *args)
			if not outputLine: continue
			outFile.write(outputLine)
			outputLineCounter += 1

		return outputLineCounter

	return newFunction


def file_batch_decorator(functionName):
	def newFunction(*args):
		for fileName in args:
			inFile = open(fileName, 'r')
			functionName(inFile)
			inFile.close()
		
		return 0
	
	return newFunction
