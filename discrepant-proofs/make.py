#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat

#------------------------
# General purpose
#------------------------

def readList(file):
	o = open(file)
	lines = o.read().splitlines()
	o.close()
	lines = filter(lambda line : line[0] != "#", lines)
	return lines

def makeExecutable(file):
	st = os.stat(file)
	os.chmod(file, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def display(message):
	print "\n@@@ " + message + "\n"

def cleanup(path):
	if os.path.exists(path):
		shutil.rmtree(path)
	os.makedirs(path)

def remove(path):
	if os.path.exists(path):
		shutil.rmtree(path)

def githubGet(name, repository, path):
	subprocess.call("wget --no-check-certificate https://github.com/" + name + "/" + repository + "/archive/master.tar.gz -P " + path, shell=True)


#------------------------
# Directory structure
#------------------------

solversPath = "solvers/"
drattrimPath = "drat-trim/"
gratgenPath = "gratgen/"
runlimPath = "runlim/"
tempPath = "temp_/"
downloadPath = "temp_/download/"
unpackPath = "temp_/unpack/"

#------------------------
# Checkers
#------------------------

def makeDratTrim():
	remove(drattrimPath)
	display("Downloading drat-trim")
	cleanup(downloadPath)
	githubGet("marijnheule", "drat-trim", downloadPath)
	display("Unpacking drat-trim")
	cleanup(unpackPath)
	subprocess.call("tar -xf " + downloadPath + "/master.tar.gz -C " + unpackPath, shell=True)
	shutil.copytree(unpackPath + "drat-trim-master/", drattrimPath)
	display("Building drat-trim")
	subprocess.call("make", cwd = drattrimPath, shell = True)
	makeExecutable(drattrimPath + "/drat-trim")

def makeGratGen():
	remove(gratgenPath)
	display("Downloading gratgen")
	cleanup(downloadPath)
	subprocess.call("wget --no-check-certificate http://www21.in.tum.de/~lammich/grat/gratgen.tgz -P " + downloadPath, shell=True)
	display("Unpacking gratgen")
	cleanup(unpackPath)
	subprocess.call("tar -xf " + downloadPath + "gratgen.tgz -C " + unpackPath, shell=True)
	shutil.copytree(unpackPath + "gratgen/", gratgenPath)
	display("Building gratgen")
	subprocess.call("cmake .", cwd = gratgenPath, shell = True)
	subprocess.call("make", cwd = gratgenPath, shell = True)
	subprocess.call("make install", cwd = gratgenPath, shell = True)

def makeCheckers():
	makeDratTrim()
	makeGratGen()

#------------------------
# Main
#------------------------

makeCheckers()
remove(tempPath)
