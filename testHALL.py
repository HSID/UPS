#! /usr/bin python

import decorators

@decorators.file_decorator
def getVfromHall(hallFile, outFile):
	time = ''
	timeStringList = []
	outputLineCounter = 0
	while True:
		line = hallFile.readline()
		if not line: break
		segments = line.split()
		second = segments[0].split('.')[0]
		if second != time:
			for timeString in timeStringList:
				outFile.write(' '.join([timeString, str(len(timeStringList))]) + '\n')
				outputLineCounter += 1 
			timeStringList = [segments[0]]
			time = second
		else:
			timeStringList.append(segments[0])
	return outputLineCounter
