# Python 2.7
#
# Insert Application layer for Wyndham
#

import csv

def getRows(fileName):
	# 1. Load CVS file
	# 2. Return row reader object
	#
	# Load CSV file	
	import os.path,csv,datetime
	csvFileName = fileName
	inFileHandle = open(csvFileName + '.csv', 'r')
	# Get the field names from the header
	crHostReader = csv.reader( inFileHandle )
	fieldnames = crHostReader.next()
	rowReader = csv.DictReader( inFileHandle, fieldnames)
	return rowReader,fieldnames

rowReader,fieldnames = getRows("techs")
csvfile = open("techsOut" + ".csv", 'w')
csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')

for row in rowReader:
	csvfileWriter.writerow(row)
	row["layer"] = "Application"
	row["component"] = "TBD"
	row["version"] = "TBD"
	csvfileWriter.writerow(row)
	




