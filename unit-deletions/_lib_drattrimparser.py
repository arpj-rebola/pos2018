import os
import sys
import fnmatch
import time
import shutil
import re

line_status = "s "
status_accept = "s VERIFIED"
status_reject = "s NOT VERIFIED"
line_unitdel = "c ignoring deletion intruction"

def getOccurrence(string, substring):
	return string.count(substring) > 0

def diagnose(parsed, filename):
	if parsed['status'] != "accept" and parsed['status'] != "reject":
		print "ERROR: Could not parse file " + filename
		return False
	else:
		return True

def is_accept(parsed):
	return parsed['status'] == "accept"

def is_reject(parsed):
	return parsed['status'] == "reject"

def get_unit_deletions(parsed):
	return parsed['unit deletions']

def parse(reader):
	status = None
	unitdels = 0
	lines = reader.read().splitlines()
	for line in lines:
		if line.startswith(line_status):
			if getOccurrence(line, status_accept):
				status = "accept"
			elif getOccurrence(line, status_reject):
				status = "reject"
			else:
				status = "un"
		if line.startswith(line_unitdel):
			unitdels = unitdels + 1
	return {'status': status, 'unit deletions' : unitdels}