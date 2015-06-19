#! /usr/bin python

import decorators

import time_utils

import re

import math

@decorators.file_decorator
@decorators.file_operation_extension_decorator
def extractOBD(line):
	"""
	line: a line of the OBD file
	return: the useful output line

	example output:
	'7.01 16'
	m/s
	"""
	segments = line.split(',')
	if len(segments) > 2 and all([re.findall(r'[0-9]+', segments[i]) for i in (1, 2)]):
		segments[2] = '%.1f' % (float(segments[2])/3.6)
		return (' '.join(segments[1:3]) + '\n')
	else: 
		return ''
	

def generateOutputStrList(distInterval, timeInterval, distRecInterval):
	"""
	"""
	(startDist, endDist) = distInterval
	(startTime, endTime) = timeInterval
	distIntervalLen = endDist - startDist
	timeIntervalLen = endTime - startTime
	startRecDist = math.ceil(startDist/distRecInterval) * distRecInterval
#	endRecDist = math.floor(endDist/distRecInterval) * distRecInterval
	outputList = []
	dist = startRecDist
	while dist < endDist:
		recordTime = (dist - startDist)/distIntervalLen * timeIntervalLen + startTime
		outputList.append('%.4f %.4f\n' % (recordTime, dist))
		dist += distRecInterval
	return outputList


@decorators.file_decorator
def getTimeDistOBD(inFile, outFile, distInterval):
	"""
	"""
	timeMemo = 0.0
	distMemo = 0.0
	outputLineCounter = 0
	while True:
		line = inFile.readline()
		if not line: break
		segmentList = line.split()
		timeCurrent = float(segmentList[0])
		velocity = float(segmentList[1])
		distCurrent = distMemo + velocity * (timeCurrent - timeMemo)
		if math.floor(distCurrent/distInterval) > math.floor(distMemo/distInterval):
			n = int(math.floor(distCurrent/distInterval) - math.floor(distMemo/distInterval))
			for i in range(n):
				dist = (math.floor(distMemo/distInterval) + i + 1) * distInterval
				time = (dist - distMemo)/velocity + timeMemo
				outFile.write(' '.join(['%.6f' % time, '%.2f' % dist]) + '\n')
				outputLineCounter += 1
			timeMemo = timeCurrent
			distMemo = distCurrent
		else:
			timeMemo = timeCurrent
			distMemo = distCurrent

	return outputLineCounter


@decorators.file_decorator
def getTimeDistHall(inFile, outFile, distPerCycle, distInterval, cyclePre):
	"""
	"""
	startTimeString = inFile.readline()
	startTime = float(time_utils.timeFormat(startTimeString))
	samplePeriod = float(inFile.readline())
	fileLen = int(inFile.readline())
	itemCounter = 0
	sampleNumBtw = 0
	cycleCounter = 0.0 - cyclePre
	startDist = 0.0
	state = 'NEGATIVE'
	outputLineCounter = 0
	
	while True:
		line = inFile.readline()
		if not line: break
		segmentList = line.split()
		if not segmentList or len(segmentList) > 1: continue
		value = float(segmentList[0])
		itemCounter += 1
		if value < 0 and state == 'POSITIVE' and (sampleNumBtw * samplePeriod > 0):
			state = 'NEGATIVE'
			timeIncrement = sampleNumBtw * samplePeriod
			sampleNumBtw = 1
			cycleCounter += 1
			endTime = startTime + timeIncrement
			endDist = cycleCounter * distPerCycle
			outputStringList = generateOutputStrList((startDist, endDist), (startTime, endTime), distInterval)
			startDist = endDist
			startTime = endTime
			for outputString in outputStringList: 
				outFile.write(outputString)
				outputLineCounter += 1
		else:
			state = ('NEGATIVE' if value < 0 else 'POSITIVE')
			sampleNumBtw += 1
	
	if itemCounter == fileLen: print 'getTimeDist: Successfully go through all record entries!'
	else: print 'getTimeDist: Missed some record entries!'
	
	return outputLineCounter 
			
