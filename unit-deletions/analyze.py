#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat
import _lib_tsvparser

def readList(file):
	o = open(file)
	lines = o.read().splitlines()
	o.close()
	lines = filter(lambda line : line[0] != "#", lines)
	return lines

def countCategory(table, category):
	cat = 0
	for row in table:
		if row['category'] == category:
			cat = cat + 1
	return cat

def countSomeDeletion(table):
	cat = 0
	for row in table:
		if row['category'] == "SSunsat_DTaccept":
			if row['drattrim_unit_deletions'] > 0:
				cat = cat + 1
	return cat

def countMoreDeletions(table, N):
	cat = 0
	for row in table:
		if row['category'] == "SSunsat_DTaccept":
			if row['drattrim_unit_deletions'] > N:
				cat = cat + 1
	return cat

def deletionFrequencies(table):
	freqs = []
	for row in table:
		if row['category'] == "SSunsat_DTaccept":
			freqs.append(row['drattrim_unit_deletions'])
	return freqs

# def cummulativeGraph(ls):
# 	sls = sorted(ls)
# 	graph = []
# 	for n in range(0, len(sls)):
# 		graph.append([n, sls[n]])
# 	return graph

# def writeTable(table, writer):
# 	for row in table:
# 		for elem in row:
# 			writer.write(str(elem))
# 			writer.write("\t")
# 		writer.write("\n")


def ratio(int1, int2):
	return str(round(float(int1) / float(int2) * 100, 1))

dashline = "----------------------------------------------------\n"

columns = []
_lib_tsvparser.addId(columns, "id")
_lib_tsvparser.addString(columns, "benchmark_solver")
_lib_tsvparser.addString(columns, "benchmark_instance")
_lib_tsvparser.addString(columns, "category")
_lib_tsvparser.addString(columns, "solver_status")
_lib_tsvparser.addFloat(columns, "solver_time")
_lib_tsvparser.addString(columns, "solver_result")
_lib_tsvparser.addString(columns, "drattrim_status")
_lib_tsvparser.addString(columns, "drattrim_time")
_lib_tsvparser.addString(columns, "drattrim_result")
_lib_tsvparser.addInteger(columns, "drattrim_unit_deletions")
o = open(sys.argv[1])
table = _lib_tsvparser.parse(o, columns)
o.close()

num_SSfailed = countCategory(table, "SSfailed")
num_SSsat = countCategory(table, "SSsat")
num_SSunsat_DTfailed = countCategory(table, "SSunsat_DTfailed")
num_SSunsat_DTaccept = countCategory(table, "SSunsat_DTaccept")
num_SSunsat_DTreject = countCategory(table, "SSunsat_DTreject")
num_SSunsat = num_SSunsat_DTfailed + num_SSunsat_DTaccept + num_SSunsat_DTreject
num_total = len(table)
num_unitdels = countSomeDeletion(table)
num_hundreddels = countMoreDeletions(table,100)
num_thousanddels = countMoreDeletions(table,1000)
delfreq = sorted(deletionFrequencies(table))
# delfreq = deletionFrequencies(table)
# delcumm = cummulativeGraph(delfreq)

print ""
print dashline + "  Result overview\n" + dashline
print "Total instances: " + str(num_total)
print "\tSAT solver did not terminate: " + str(num_SSfailed) + " (" + ratio(num_SSfailed, num_total) + "%)"
print "\tSAT solver reported satisfiable: " + str(num_SSsat) + " (" + ratio(num_SSsat, num_total) + "%)"
print "\tSAT solver reported unsatisfiable: " + str(num_SSunsat) + " (" + ratio(num_SSunsat, num_total) + "%)"
print "\t\tDRAT-trim did not terminate: " + str(num_SSunsat_DTfailed) + " (" + ratio(num_SSunsat_DTfailed, num_SSunsat) + "%)"
print "\t\tDRAT-trim rejected proof: " + str(num_SSunsat_DTreject) + " (" + ratio(num_SSunsat_DTreject, num_SSunsat) + "%)"
print "\t\tDRAT-trim accepted proof: " + str(num_SSunsat_DTaccept) + " (" + ratio(num_SSunsat_DTaccept, num_SSunsat) + "%)"
print "\t\t\tDRAT-trim ignored unit deletions: " + str(num_unitdels) + " (" + ratio(num_unitdels, num_SSunsat_DTaccept) + "%)"
print "\t\t\tDRAT-trim ignored more than 100 unit deletions: " + str(num_hundreddels) + " (" + ratio(num_hundreddels, num_SSunsat_DTaccept) + "%)"
print "\t\t\tDRAT-trim ignored more than 1000 unit deletions: " + str(num_thousanddels) + " (" + ratio(num_thousanddels, num_SSunsat_DTaccept) + "%)"
print "\t\t\tMaximum amount of unit deletions: " + str(delfreq[len(delfreq) - 1])


# print ""
# print dashline + "  Distribution of unit deletions\n" + dashline
# o = open(sys.argv[2] + ".dat", 'w')
# writeTable(delcumm, o)
# o.close()
# print "Table written to " + sys.argv[2] + ".dat" 
