#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat

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

def remove(path):
	if os.path.exists(path):
		shutil.rmtree(path)

directoriesPath = "info/directories.txt"
directoriesList = readList(directoriesPath)
benchmarksPath = directoriesList[0]
tempPath = "temp_/"

cleanup(benchmarksPath)
subprocess.call("wget --no-check-certificate https://baldur.iti.kit.edu/sat-competition-2017/benchmarks/Main.zip -P " + tempPath, shell=True)
subprocess.call("unzip " + tempPath + "Main -d " + benchmarksPath, shell=True)
remove(tempPath)
files = os.listdir(benchmarksPath + "NoLimits")
for file in files:
	shutil.move(benchmarksPath + "NoLimits/" + file, benchmarksPath)
remove(benchmarksPath + "NoLimits")
