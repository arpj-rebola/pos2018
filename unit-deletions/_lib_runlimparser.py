import os
import sys
import fnmatch
import time
import shutil
import re

line_status = "[runlim] status:"
line_time = "[runlim] real:"
status_ok = "ok"
status_to = "out of time"
status_mo = "out of memory"
status_un = "unknown"

def getOccurrence(string, substring):
	return string.count(substring) > 0

def getDecimal(string):
	decimals = re.findall("\d+\.\d+", string)
	return float(decimals[0])

def diagnose(parsed, filename):
	if parsed['status'] != "ok" and parsed['status'] != "to" and parsed['status'] != "mo":
		print "ERROR: Could not parse file x " + filename
		return False
	elif parsed['time'] == None:
		print "ERROR: Could not parse file y " + filename
		return False
	else:
		return True

def is_ok(parsed):
	return parsed['status'] == "ok"

def is_timeout(parsed):
	return parsed['status'] == "to"

def is_memout(parsed):
	return parsed['status'] == "mo"

def get_time(parsed):
	return parsed['time']

def parse(reader):
	status = None
	time = None
	lines = reader.read().splitlines()
	for line in lines:
		if line.startswith(line_status):
			line = line[len(line_status):]
			if getOccurrence(line, status_ok):
				status = "ok"
			elif getOccurrence(line, status_to):
				status = "to"
			elif getOccurrence(line, status_mo):
				status = "mo"
			else:
				status = "un"
		elif line.startswith(line_time):
			line = line[len(line_time):]
			time = getDecimal(line)
	return {'status': status, 'time': time}
