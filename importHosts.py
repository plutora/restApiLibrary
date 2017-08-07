## Import Hosts from CSV file
#
import plutora,csv

## Create Hosts from CSV file and document the results in a new CSV file with the Host GUID
import os.path,csv,datetime
csvFileName = 'hosts'

# Load CSV file	
crHostFile = open(csvFileName + '.csv', 'r')
# Get the field names from the header
crHostReader = csv.reader( crHostFile )
fieldnames = crHostReader.next()
dictReader = csv.DictReader( crHostFile, fieldnames)
# Create output file name with timestamp
outfile = open(csvFileName + '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()) + '.csv', 'w')
# TODO: remove the following line...
dictReader = csv.DictReader( crHostFile, fieldnames)
# Add envGuid row to outfile
fieldnames.append('hostGuid')
fieldnames.append('layerGuid')
writer = csv.DictWriter(outfile, fieldnames=fieldnames, lineterminator='\n')
writer.writeheader()

# Read in each row for processing
# TODO: Accommodate hierarchical object processing:
#  Two styles:  
#	(1) Column values repeated and
#		col1	col2
#		top1	vala
#		top1	valb
#		top2	valc
#
#	(2) First column value then blanks
#		col1	col2
#		top1
#				vala
#				valb
#		top2
#				valc

environments = plutora.listToDict(plutora.api("GET","environments"), "name", "id")
layers = plutora.listToDict(plutora.api("GET","lookupfields/StackLayer"), "value", "id")

for row in dictReader:
	myHost = {
		'name': row['host'],
		'EnvironmentID': environments[row['environment']]
	}
	
	host = plutora.api("POST", "hosts", myHost)
	hostApi = "hosts/" + host['id']
	print "Created " + hostApi + " - " + host['name']
	row['hostGuid']=host['id']
	
	myLayer = {
		"ComponentName": row['component'],
		"Version": row['version'],
		"HostID": host['id'],
		"EnvironmentID": environments[row['environment']],
		"StackLayerID": layers[row['layer']+" Layer"]
	}
	layer = plutora.api("POST", "layers", myLayer)
	print layer
	layerApi = "layers/" + layer['id']
	print "Created " + layerApi + " - " + layer['componentName']
	row['layerGuid']=layer['id']
	writer.writerow(row)
	
crHostFile.close()