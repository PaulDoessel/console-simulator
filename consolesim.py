from __future__ import print_function

import sys
import json
import fileinput
import random
import time
import string
import traceback
import os


class ConsoleSimulator:

	def __init__(self):
		self.processStates = []
		self.minTimePerLine = 200
		self.maxTimePerLine = 300
		self.prefix = "starting"
		self.suffix = "finishing"
		self.preambleFile = "PreambleFile.txt"
		self.dataFile = "DataFile.txt"
		self.loopFileCount = 1


	def fixLine(self, text):
		s = ""
		for c in text:
			if c == '#':
				s += random.SystemRandom().choice(string.digits)
			else:
				s += c
		return s

	def writeProgressPause(self, progressIndicator, sleep):
		if progressIndicator > 0:
			sleepGap = sleep / progressIndicator
			for i in range(0, progressIndicator):
				self.write(".")
				time.sleep(sleepGap / 1000.0)
		else:
			time.sleep(sleep / 1000.0)


	def write(self, line = ''):
		print (line, end='')
		sys.stdout.flush()

	def writeLine(self, line = ''):
		print (line)


	def processFile(self, filename, writeInitialPrefix):

		if writeInitialPrefix:
			self.writeProgressPause(5, self.minTimePerLine)
	
		self.write()
	
		for line in fileinput.input(filename):
			line = line.rstrip()
			sleepTimePerLine = random.SystemRandom().choice(range(self.minTimePerLine, self.maxTimePerLine))
			if len(line) == 0:
				self.writeLine()
			elif line.startswith('*'):
				self.writeLine(line[1:])
				self.writeProgressPause(0, sleepTimePerLine)
			else:
			
				sleepTimePerLineSegment = sleepTimePerLine / len(self.processStates)
				self.write(self.fixLine(line))
		
				for state in self.processStates:
					self.writeProgressPause(5, sleepTimePerLineSegment)
					self.write(self.fixLine(state))
			
				self.writeLine(" (" + str(sleepTimePerLine) + "ms)")
	
			self.writeLine()

	def run(self):
		self.writeLine(self.prefix)

		self.processFile(self.preambleFile, False)

		for i in range(0, self.loopFileCount):
			self.processFile(self.dataFile, True)
	

		self.writeLine(self.suffix)


os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

print(os.getcwd())

try:
	config = json.load(open('./consolesim.config')) 

	cs = ConsoleSimulator()
	cs.processStates = config['ProcessingLineSuffix'].split(",")
	cs.minTimePerLine = config['MinTimePerLine']
	cs.maxTimePerLine = config['MaxTimePerLine']
	cs.prefix = config['ProgramPrefix']
	cs.suffix = config['ProgramSuffix']
	cs.loopFileCount = config['LoopFileCount']
	cs.preambleFile = config['PreambleFile']
	cs.dataFile = config['DataFile']
	cs.run()
	
except KeyboardInterrupt:
	writeLine("Shutdown requested...exiting")
except Exception:
	traceback.print_exc(file=sys.stdout)
sys.exit(0)
