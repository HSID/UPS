#!/env/bin python

import re
import decorators

@decorators.file_decorator
@decorators.file_operation_extension_decorator
def extractGSM(line):
	"""
	line: a line of string of the raw osmocombb file 

	output example:
	"1399641464.4 63:41"
	"""
	numberList = re.findall(r'([0-9]+) +([0-9]+) +L1CTL_PM_REQ +start=([0-9]+) +end=([0-9]+)', line)
	if numberList:
		return (' '.join(['.'.join(numberList[0][:2]), '-'.join(numberList[0][2:])]) + '\n')
	numberList = re.findall(r'([0-9]+) +([0-9]+) +PM +MEAS: +ARFCN=([0-9]+), +([0-9]+) +dBm', line)
	if numberList: 
		return (' '.join(['.'.join(numberList[0][:2]), ':'.join(numberList[0][2:])]) + '\n')
	return ''


@decorators.file_decorator
@decorators.file_operation_extension_decorator			
def extractEffectiveLine(line):
	"""
	line: a line of string of the raw osmocombb file

	output the effective line of the raw osmocombb file
	"""
	return (line if line.find('end') != -1 or line.find('ARFCN') != -1 else '')

@decorators.file_batch_decorator
def channelSeparate(inFile):
	"""
	"""
	fileDict = {}

	while True:
		line = inFile.readline()
		if not line: break
		segmentList = line.split()
		if segmentList[1].find(':') != -1:
			channelID = segmentList[1].split(':')[0]
			if 'channel' + channelID in fileDict:
				fileDict['channel' + channelID].write(line)
			else: 
				fileDict['channel' + channelID] = open('channel' + channelID, 'w')

	for fileName in fileDict:
		fileDict[fileName].close()

	return 0
			
			
	
