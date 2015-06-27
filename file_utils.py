#! /env/bin python

import decorators
import time_utils

@decorators.file_decorator
@decorators.file_operation_extension_decorator
def timeAdjust(line, time_offset):
	"""
	change the timestamp value of each file entry
	"""
	segments = line.split()
	segments[0] = '%.6f' % (float(segments[0]) + time_offset)
	
	return (' '.join(segments) + '\n')


@decorators.file_decorator
@decorators.file_operation_extension_decorator
def timeFormalize(line):
	"""
	change the timestamp format of the file
	especially for the smart phone logger records
	"""
	segments = line.split()
	segments[0] = time_utils.timeFormat(segments[0])

	return (' '.join(segments) + '\n')

@decorators.file_decorator
def removeIdentLine(inFile, outFile):
	preLine = ''
	while True:
		line = inFile.readline()
		if not line: break
		if line != preLine:
			outFile.write(line)
		preLine = line

@decorators.file_decorator
@decorators.file_operation_extension_decorator
def reformGSMVector(line):
	"""
	sort the GSM vector according to the channel ID
	"""
	segments = line.split()
	segments = [item[(item.find(':') + 1):]\
				if ':' in item\
				else item\
				for item in segments]

	return (' '.join(segments) + '\n')

@decorators.file_decorator
@decorators.file_operation_extension_decorator
def extractLine(line, lineID):
	"""
	"""
	segmentList = line.split()
	outputSegments = [segmentList[i] for i in lineID]
	
	return (' '.join(outputSegments) + '\n')


def mergeFile(refFile, outputFile, *otherFiles):
	candidates = [[None, None] for i in range(len(otherFiles))]
	while True:
		line = refFile.readline()
		if not line: break
		(time_str, value_str) = (line.split()[0], ' '.join(line.split()[1:]))
		outputLine = time_str + ' ' + value_str
		for i in range(len(otherFiles)):
			while True:
				if all(candidates[i]):
					if float(time_str) < float(candidates[i][1][0]):
						if abs(float(time_str) - float(candidates[i][0][0])) <= abs(float(time_str) - float(candidates[i][1][0])):
							outputLine = outputLine + ' ' + candidates[i][0][1]
							break
						else:
							outputLine = outputLine + ' ' + candidates[i][1][1]
							candidates[i][0] = None
							break
					else:
						candidates[i][0] = candidates[i][1]
						candidates[i][1] = None
				elif candidates[i][0] != None:
					line = otherFiles[i].readline()
					if not line: 
						outputLine = outputLine + ' ' + candidates[i][0][1]
						break
					(time_str_c, value_str_c) = (line.split()[0], ' '.join(line.split()[1:]))
					if float(time_str) > float(time_str_c):
						candidates[i][0] = (time_str_c, value_str_c)
					else:
						candidates[i][1] = (time_str_c, value_str_c)
				elif candidates[i][1] != None:
					if float(time_str) < float(candidates[i][1][0]):
						outputLine = outputLine + ' ' + candidates[i][1][1]
						break
					else:
						line = otherFiles[i].readline()
						if not line:
							outputLine = outputLine + ' ' + candidates[i][1][1]
							break
						(time_str_c, value_str_c) = (line.split()[0], ' '.join(line.split()[1:]))
						if float(time_str) < float(time_str_c):
							candidates[i][0] = candidates[i][1]
							candidates[i][1] = (time_str_c, value_str_c)
						else:
							candidates[i][0] = (time_str_c, value_str_c)
							candidates[i][1] = None
				else:
					line = otherFiles[i].readline()
					if not line: break
					(time_str_c, value_str_c) = (line.split()[0], ' '.join(line.split()[1:]))
					if float(time_str) < float(time_str_c):
						candidates[i][1] = (time_str_c, value_str_c)
						outputLine = outputLine + ' ' + candidates[i][1][1]
						break
					else:
						candidates[i][0] = (time_str_c, value_str_c)
		outputFile.write(outputLine + '\n')				

