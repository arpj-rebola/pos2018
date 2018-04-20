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
runlimPath = "runlim/"
tempPath = "temp_/"
downloadPath = "temp_/download/"
unpackPath = "temp_/unpack/"

#------------------------
# Solvers
#------------------------

def downloadSolver(solver):
	display("Downloading solver " + solver)
	cleanup(downloadPath)
	subprocess.call("wget https://baldur.iti.kit.edu/sat-competition-2017/solvers/main/" + solver + ".zip -P " + downloadPath, shell=True)

def unpackSolver(solver):
	display("Unpacking solver " + solver)
	cleanup(unpackPath)
	subprocess.call("unzip " + downloadPath + solver + ".zip -d " + unpackPath, shell=True)
	if solver == "Riss7":
		variants = ["Riss7_BVE", "Riss7_noPP"]
		unpackedpath = unpackPath
	elif solver == "satUZK-seq":
		variants = ["satUZK-seq_ge", "satUZK-seq_me", "satUZK-seq_sge", "satUZK-seq_sme"]
		unpackedpath = unpackPath
	else:
		variants = [solver]
		unpackedpath = unpackPath + solver
	for variant in variants:
		remove(solversPath + variant)
		shutil.copytree(unpackedpath, solversPath + variant)

def buildSolver(solver):
	display("Building solver " + solver)
	if solver != "Riss7" and solver != "satUZK-seq":
		makeExecutable(solversPath + solver + "/starexec_build")
		if solver == "cadical-sc17-agile-proof" or solver == "cadical-sc17-proof" or solver == "lingeling-bbe":
			makeExecutable(solversPath + solver + "/build/build.sh")
		if solver == "CandyRSILi" or solver == "CandyRSILv":
			# this must be executed after Candy has been processed...
			shutil.copytree(solversPath + "Candy/lib/googletest", solversPath + solver + "/lib/googletest")
		subprocess.call("./starexec_build", cwd=solversPath + solver, shell=True)
	if solver == "Riss7":
		makeExecutable(solversPath + "Riss7_BVE/bin/riss")
		makeExecutable(solversPath + "Riss7_noPP/bin/riss")
	if solver == "bs_glucose":
		makeExecutable(solversPath + "bs_glucose/bin/bs_glucose1")
	if solver == "satUZK-seq":
		makeExecutable(solversPath + "satUZK-seq_ge/bin/satUZK-seq")
		makeExecutable(solversPath + "satUZK-seq_sge/bin/satUZK-seq")
		makeExecutable(solversPath + "satUZK-seq_me/bin/satUZK-seq")
		makeExecutable(solversPath + "satUZK-seq_sme/bin/satUZK-seq")
	if solver == "tch_glucose1":
		makeExecutable(solversPath + "tch_glucose1/bin/tch_glucose1")
	if solver == "tch_glucose2":
		makeExecutable(solversPath + "tch_glucose2/bin/tch_glucose2")
	if solver == "tch_glucose3":
		makeExecutable(solversPath + "tch_glucose3/bin/tch_glucose3")

def makeSolvers():
	cleanup(solversPath)
	solvers = readList("info/download-list.txt")
	for solver in solvers:
		downloadSolver(solver)
		unpackSolver(solver)
		buildSolver(solver)

#------------------------
# Checkers
#------------------------

def downloadChecker():
	display("Downloading drat-trim ")
	cleanup(downloadPath)
	githubGet("marijnheule", "drat-trim", downloadPath)

def unpackChecker():
	display("Unpacking drat-trim")
	cleanup(unpackPath)
	subprocess.call("tar -xf " + downloadPath + "/master.tar.gz -C " + unpackPath, shell=True)
	shutil.copytree(unpackPath + "drat-trim-master/", drattrimPath)

def buildChecker():#
	display("Building drat-trim")
	subprocess.call("make", cwd = drattrimPath, shell = True)
	makeExecutable(drattrimPath + "/drat-trim")

def makeCheckers():
	remove(drattrimPath)
	downloadChecker()
	unpackChecker()
	buildChecker()

#------------------------
# Runlim
#------------------------

def makeRunlim():
	remove(runlimPath)
	display("Unpacking runlim")
	cleanup(unpackPath)
	subprocess.call("tar -xf runlim-1.12.tar.gz -C " + unpackPath, shell=True)
	print unpackPath + "runlim-1.12"
	print runlimPath
	shutil.copytree(unpackPath + "runlim-1.12/", runlimPath)
	display("Building runlim")
	subprocess.call("./configure.sh", cwd=runlimPath, shell=True)
	subprocess.call("make", cwd=runlimPath, shell=True)

#------------------------
# Scripts
#------------------------

def writeDirectories(ls, path):
	xls = []
	for x in ls:
		if(x[-1] == "/"):
			xls.append(x)
		else:
			xls.append(x + "/")
	if os.path.exists(path):
		os.remove(path)
	o = open(path, 'w')
	for x in xls:
		o.write(x + "\n")
	o.close()

def writePairs(solverspath, instancespath, outputpath):
	if os.path.exists(outputpath):
		os.remove(outputpath)
	solvers = readList(solverspath)
	instances = readList(instancespath)
	finallist = []
	counter = 1
	o = open(outputpath, 'w')
	for solver in solvers:
		for instance in instances:
			o.write(str(counter) + " " + solver + " " + instance + "\n")
			counter = counter + 1
	o.close()

def generateSubmit():
	if os.path.exists("submit.sh"):
		os.remove("submit.sh")
	o = open("submit.sh", 'w')
	o.write("""#!/bin/sh
die () {
  echo "*** submit.sh: $*" 1>&2
  exit 1
}
msg () {
  echo "[submit.sh] $*"
}
[ -f info/pairs.txt ] || die "could not find 'info/pairs.txt'"
jobs=`wc -l info/pairs.txt |awk '{print $1}'`
msg "submitting $jobs pairs"
sbatch -a "1-$jobs" array.sh
""")
	o.close()
	makeExecutable("submit.sh")

def generateArray(directory):
	if os.path.exists("array.sh"):
		os.remove("array.sh")
	o = open("array.sh", 'w')
	o.write("""#!/bin/sh
#SBATCH -J adrian
#SBATCH -c 4
#SBATCH -o /dev/null
#SBATCH -e /dev/null
SOLVER="`awk '$1 == "'$SLURM_ARRAY_TASK_ID'"{print $2}' info/pairs.txt`"
INSTANCE="`awk '$1 == "'$SLURM_ARRAY_TASK_ID'"{print $3}' info/pairs.txt`"
NAME="$INSTANCE.$SOLVER"
exec 1>""" + directory + """"$NAME".log 2>""" + directory + """"$NAME".err
echo "array.sh: $SOLVER $INSTANCE `hostname`"
exec ./experiment.py $SOLVER $INSTANCE
""")
	o.close()
	makeExecutable("array.sh")

def generateScripts(directory):
	writePairs("info/solver-list.txt", "info/instances.txt", "info/pairs.txt")
	generateSubmit()
	generateArray(directory)

#------------------------
# Main
#------------------------

display("Storing directory paths")
paths = [sys.argv[1], sys.argv[2], sys.argv[3]]
writeDirectories(paths, "info/directories.txt")
display("Generating SBATCH scripts")
generateScripts(sys.argv[2])
makeSolvers()
makeCheckers()
makeRunlim()
remove(tempPath)
