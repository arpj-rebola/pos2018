import os
import sys
import fnmatch
import time
import shutil
import re

id_type = "id"
string_type = "string"
integer_type = "integer"
float_type = "float"

def addId(columns, name):
	columns.append([name, id_type])

def addString(columns, name):
	columns.append([name, string_type])

def addInteger(columns, name):
	columns.append([name, integer_type])

def addFloat(columns, name):
	columns.append([name, float_type])

def getData(read, datatype):
	if read == "NULL":
		return None
	elif datatype == id_type or datatype == integer_type:
		return int(read)
	elif datatype == string_type:
		return read
	elif datatype == float_type:
		return float(read)


def parse(reader, columns):
	lines = filter(lambda line: len(line) > 0 and line[0] != "#", reader.read().splitlines())
	table = []
	for line in lines:
		data = {}
		spline = line.split("\t")
		for i in range(0,len(columns)):
			[name, datatype] = columns[i]
			data[name] = getData(spline[i], datatype)
		table.append(data)
	return table
