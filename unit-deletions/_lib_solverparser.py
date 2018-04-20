import os
import sys
import fnmatch
import time
import shutil
import re

line_status = "s "
status_sat = "s SATISFIABLE"
status_unsat = "s UNSATISFIABLE"

def getOccurrence(string, substring):
	return string.count(substring) > 0

def diagnose(parsed, filename):
	if parsed['status'] != "sat" and parsed['status'] != "unsat":
		print "ERROR: Could not parse file " + filename
		return False
	else:
		return True

def is_sat(parsed):
	return parsed['status'] == "sat"

def is_unsat(parsed):
	return parsed['status'] == "unsat"

def parse(reader):
	status = None
	lines = reader.read().splitlines()
	for line in lines:
		if line.startswith(line_status):
			if getOccurrence(line, status_sat):
				status = "sat"
			elif getOccurrence(line, status_unsat):
				status = "unsat"
			else:
				status = "un"
	return {'status': status}