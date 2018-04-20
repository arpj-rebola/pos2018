#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat

def runDratTrim(formula, proof):
	subprocess.call("./drat-trim/drat-trim " + formula + " " + proof, shell = True)

def runGratGen(formula, proof):
	subprocess.call("./gratgen/gratgen " + formula + " " + proof, shell = True)

print ""
print "\"formula.cnf\" contains a CNF formula in DIMACS format."
print "\"specified.drat\" contains a correct (specified) DRAT refutation of \"formula.cnf\"."
print "\"operational.drat\" contains an incorrect (specified) DRAT refutation of \"formula.cnf\"."
print ""
print "Running DRAT-trim over DIMACS formula \"formula.cnf\" and correct (specified) DRAT refutation \"specified.drat\" (should reject the proof)"
raw_input("Press any key to continue...")
runDratTrim("formula.cnf", "specified.drat")
raw_input("Press any key to continue...")
print ""
print "Running DRAT-trim over DIMACS formula \"formula.cnf\" and incorrect (specified) DRAT refutation \"operational.drat\" (should accept the proof)"
raw_input("Press any key to continue...")
runDratTrim("formula.cnf", "operational.drat")
raw_input("Press any key to continue...")
print ""
print ""
print "Running gratgen over DIMACS formula \"formula.cnf\" and correct (specified) DRAT refutation \"specified.drat\" (should reject the proof)"
raw_input("Press any key to continue...")
runGratGen("formula.cnf", "specified.drat")
raw_input("Press any key to continue...")
print ""
print "Running gratgen over DIMACS formula \"formula.cnf\" and incorrect (specified) DRAT refutation \"operational.drat\" (should accept the proof)"
raw_input("Press any key to continue...")
runGratGen("formula.cnf", "operational.drat")
raw_input("Press any key to continue...")