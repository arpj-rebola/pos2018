#! /usr/bin/env python

import os
import sys
import fnmatch
import time
import shutil
import subprocess
import stat
import _lib_runlimparser
import _lib_solverparser
import _lib_drattrimparser

def readList(file):
	o = open(file)
	lines = o.read().splitlines()
	o.close()
	lines = filter(lambda line : line[0] != "#", lines)
	return lines

directoryList = readList("info/directories.txt")
outputPath = directoryList[1]

def solverOutputPath(solver, instance):
	return outputPath + instance + "." + solver + ".SS.out"

def checkerOutputPath(solver, instance):
	return outputPath + instance + "." + solver + ".DT.out"

def solverRunlimPath(solver, instance):
	return outputPath + instance + "." + solver + ".SS.run"

def checkerRunlimPath(solver, instance):
	return outputPath + instance + "." + solver  + ".DT.run"

def checkExistence(path):
	if not os.path.exists(path):
		print "ERROR: could not find file " + path
	return os.path.exists(path)

def writeTsv(path, results, columns):
	o = open(path, 'w')
	o.write("# Column 2: solver used to generate DRAT proof\n")
	o.write("# Column 3: SAT Competition 2017 CNF benchmark\n")
	o.write("# Column 4: instance status:\n")
	o.write("#\tSSfailed: SAT solver failed (run out of time/memory)\n")
	o.write("#\tSSsat: SAT solver reported instance as satisfiable\n")
	o.write("#\tSSunsat_DTfailed: SAT solver reported instance as unsatisfiable, DRAT-trim failed to check proof (run out of time/memory)\n")
	o.write("#\tSSunsat_DTaccept: SAT solver reported instance as unsatisfiable, DRAT-trim accepted proof\n")
	o.write("#\tSSunsat_DTreject: SAT solver reported instance as unsatisfiable, DRAT-trim rejected proof\n")
	o.write("# Columns 5, 8: result from runlim on solver and DRAT-trim respectively:\n")
	o.write("#\tok: tool terminated\n")
	o.write("#\tto: tool exceeded time limit\n")
	o.write("#\tmo: tool exceeded memory limit\n")
	o.write("#\tun: failed to parse runlim output\n")
	o.write("# Columns 6, 9: solving or checking time, respectively (in seconds)\n")
	o.write("# Column 7: SAT solver result (sat / unsat)\n")
	o.write("# Column 10: DRAT-trim result\n")
	o.write("# Column 11: number of reportedly ignored unit clause deletions in DRAT-trim\n")
	for result in results:
		o.write(result['id'])
		for column in columns:
			o.write("\t")
			if column in result:
				item = str(result[column])
			else:
				item = "NULL"
			o.write(item)
		o.write("\n")
	o.close()



def processInstance(number, solver, instance):
	out = {}
	out['id'] = number
	out['benchmark_solver'] = solver
	out['benchmark_instance'] = instance
	if not checkExistence(solverRunlimPath(solver, instance)):
		return None
	o = open(solverRunlimPath(solver, instance))
	ss_run_parsing = _lib_runlimparser.parse(o)
	o.close()
	if not _lib_runlimparser.diagnose(ss_run_parsing, solverRunlimPath(solver, instance)):
		return None
	out['solver_status'] = ss_run_parsing['status']
	out['solver_time'] = ss_run_parsing['time']
	if not _lib_runlimparser.is_ok(ss_run_parsing):
		out['category'] = "SSfailed"
		return out
	if not checkExistence(solverOutputPath(solver, instance)):
		return None
	o = open(solverOutputPath(solver, instance))
	ss_out_parsing = _lib_solverparser.parse(o)
	o.close()
	if not _lib_solverparser.diagnose(ss_out_parsing,solverOutputPath(solver, instance)):
		return None
	out['solver_result'] = ss_out_parsing['status']
	if _lib_solverparser.is_sat(ss_out_parsing):
		out['category'] = "SSsat"
		return out
	if not checkExistence(checkerRunlimPath(solver, instance)):
		return None
	o = open(checkerRunlimPath(solver, instance))
	dt_run_parsing = _lib_runlimparser.parse(o)
	o.close()
	if not _lib_runlimparser.diagnose(dt_run_parsing, checkerRunlimPath(solver, instance)):
		return None
	out['drattrim_status'] = dt_run_parsing['status']
	out['drattrim_time'] =dt_run_parsing['time']
	if not _lib_runlimparser.is_ok(dt_run_parsing):
		out['category'] = "SSunsat_DTfailed"
		return out
	if not checkExistence(checkerOutputPath(solver, instance)):
		return None
	o = open(checkerOutputPath(solver, instance))
	dt_out_parsing = _lib_drattrimparser.parse(o)
	o.close()
	if not _lib_drattrimparser.diagnose(dt_out_parsing, checkerOutputPath(solver, instance)):
		return None
	out['drattrim_result'] = dt_out_parsing['status']
	out['drattrim_unit_deletions'] = dt_out_parsing['unit deletions']
	if _lib_drattrimparser.is_accept(dt_out_parsing):
		out['category'] = "SSunsat_DTaccept"
	else:
		out['category'] = "SSunsat_DTreject"
	return out

stringList = readList("info/pairs.txt")
pairList = map(lambda x: x.split(), stringList)
results = []
for [number, solver, instance] in pairList:
	result = processInstance(number, solver, instance)
	if result != None:
		results.append(result)
writeTsv(sys.argv[1], results, ["benchmark_solver", "benchmark_instance", "category", "solver_status", "solver_time", "solver_result", "drattrim_status", "drattrim_time", "drattrim_result", "drattrim_unit_deletions"])
