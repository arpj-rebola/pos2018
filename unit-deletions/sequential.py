#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat
import random

def readList(file):
	o = open(file)
	lines = o.read().splitlines()
	o.close()
	lines = filter(lambda line : line[0] != "#", lines)
	return lines

def cleanup(path):
	if os.path.exists(path):
		shutil.rmtree(path)
	os.makedirs(path)

directoryList = readList("info/directories.txt")
outputPath = directoryList[1]
proofsPath = directoryList[2]
cleanup(outputPath)
cleanup(proofsPath)
stringList = readList("info/pairs.txt")
pairList = map(lambda x: x.split(), stringList)
if len(sys.argv) >= 2:
	pairList = random.sample(pairList, int(sys.argv[1]))
	print "sequential.py: selected random sample of " + sys.argv[1] + "instances"
	for [number, solver, instance] in pairList:
		print "sequential.py:\t\t [" + number + "] " + solver + " " + instance
for [number, solver, instance] in pairList:
	print "sequential.py: running experiment for " + solver + " " + instance
	subprocess.call("./experiment.py " + solver + " " + instance, shell=True)
