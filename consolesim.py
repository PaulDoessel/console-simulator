from __future__ import print_function

import sys
import json
import fileinput
import random
import time
import string

class ConsoleSimulator:

	def __init__(self1, str):
		self1.s = str
	def show(self1):
		print(self1.s)
	def showMsg (self, msg):
		print (msg + ':', self.show())


def fixLine(text):
	s = ""
	for c in text:
		if c == '#':
			s += random.SystemRandom().choice(string.digits)
		else:
			s += c
	return s

def writeProgressPause(progressIndicator, sleep):
	if progressIndicator > 0:
		sleepGap = sleep / progressIndicator
		for i in range(0, progressIndicator):
			write(".")
			time.sleep(sleepGap / 1000.0)
	else:
		time.sleep(sleep / 1000.0)


def write( line = ''):
	print (line, end='')
	sys.stdout.flush()

def writeLine(line = ''):
	print (line)

# have these set on class later    
config = json.load(open('consolesim.config')) 
processStates = config['ProcessingLineSuffix'].split(",")
minTimePerLine = config['MinTimePerLine']
maxTimePerLine = config['MaxTimePerLine']
prefix = config['ProgramPrefix']
suffix = config['ProgramSuffix']
loopFileCount = config['LoopFileCount']

def processFile(filename, writeInitialPrefix):

	if writeInitialPrefix:
		writeProgressPause(5, minTimePerLine)
	
	write()
	
	for line in fileinput.input(filename):
		line = line.rstrip()
		sleepTimePerLine = random.SystemRandom().choice(range(minTimePerLine, maxTimePerLine))
		if len(line) == 0:
			writeLine()
		elif line.startswith('*'):
			writeLine(line[1:])
			writeProgressPause(0, sleepTimePerLine)
		else:
			
			sleepTimePerLineSegment = sleepTimePerLine / len(processStates)
			write(fixLine(line))
		
			for state in processStates:
				writeProgressPause(5, sleepTimePerLineSegment)
				write(fixLine(state))
			
			writeLine(" (" + str(sleepTimePerLine) + "ms)")
	
		writeLine()

try:
	writeLine(prefix)

	processFile(config['PreambleFile'], False)

	for i in range(0, loopFileCount):
		processFile(config['DataFile'], True)
	

	writeLine(suffix)
except KeyboardInterrupt:
	writeLine("Shutdown requested...exiting")
except Exception:
	traceback.print_exc(file=sys.stdout)
sys.exit(0)

