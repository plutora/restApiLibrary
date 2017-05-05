# Plutora REST API Samples and test cases
# 	Several examples are provided below.  Change the "if False:" to "if True:" to
#   enable the example.

import plutora
		
# Test cases for functions

if False: # Set test value to True to run example
	## Get list of System names with GET
	systems = plutora.api("GET", "systems")
	for system in systems:
		print system['name']

if False: # Set test value to True to run example
	# Look up a system GUID by system name
	systems = plutora.api("GET", "systems")
	# Get the name of an existing System
	firstSystemName=systems[0]['name']
	sysGuidList=plutora.listToDict(systems,"name","id")
	# Show only first found GUID for System name (Plutor allows for multiple Systems with the same name)
	print "GUID for System name " + firstSystemName + " = " + sysGuidList[firstSystemName]

if False: # Set test value to True to run example
	# Look up a GUID by API path and object name
	apiPath = "organizations"
	# Get the name of an existing organization
	orgName = plutora.api("GET", apiPath)[0]['name']
	objectGuid = plutora.guidByPathAndName(apiPath, orgName)
	print "GUID of \"" + orgName + "\" of " + apiPath + " = " + objectGuid

if False: # Set test value to True to run example
	## Create a System and Enviroment with POST
	mySys = {
		"Name": "My API System",
		"Vendor": "Plutora",
		"Status": "Active",
		"OrganizationId": plutora.guidByPathAndName("organizations",plutora.api("GET", "organizations")[0]['name']) # Top level orgName
	}
	sys = plutora.api("POST", "systems", mySys)
	sysApi="systems/" + sys['id']
	print sysApi
	DevGuid = plutora.guidByPathAndName("lookupfields/UsedForWorkItem","Dev","value")
	ActiveGuid = plutora.guidByPathAndName("lookupfields/EnvironmentStatus","Active","value")
	myEnv = {
		"Name": "My API Environment",
		"Vendor": "Plutora",
		"UsageWorkItemId": DevGuid,
		"EnvironmentStatusId": ActiveGuid,
		"Color": "#ffffff",
		"IsSharedEnvironment": "true"
	}
	myEnv['LinkedSystemId']=sys['id']
	env = plutora.api("POST", "environments", myEnv)
	envApi = "environments/" + env['id']
	print envApi
	
if False: # Set test value to True to run example
	## Change values on a System with PUT
	systemApi = "systems/" + plutora.guidByPathAndName("systems","My API System")
	system = plutora.api("GET", systemApi)
	print system['name']
	system['description']="New description from API 2.0"
	# Remove the additionalInformation array from datastructure; these values not affected by PUT systems
	system.pop('additionalInformation', None)
	plutora.api("PUT", systemApi, system)
	print plutora.api("GET", systemApi, system)['description']
	
if False: # Set test value to True to run example
	## Delete an Enviroment with DELETE
	# (Systems are getting removed from the UI, but not the database: https://home.strykaqa.com/defects/P-D-1415)
	envApi = "environments/" + plutora.guidByPathAndName("environments","My API Environment")
	print plutora.api("GET", envApi)
	print "Deleting " + envApi
	print plutora.api("DELETE", envApi)

if False: # Set test value to True to run example
	## Create Environments from CSV file and document the results in a new CSV file with the Enviroment GUID
	import os.path,csv,datetime
	csvFileName = 'envs.csv'
	# Create CSV file if it doesn't already exist
	if not os.path.isfile(csvFileName):
		# Define CSV file column names
		fieldnames = [
			"sysGuid",
			"envName"
			]
		print "Creating CSV file for input"
		csvfile = open(csvFileName, 'w')
		csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
		csvfileWriter.writeheader()
		sysGuid=plutora.guidByPathAndName("systems","My API System")
		csvfileWriter.writerow({"sysGuid":sysGuid,"envName":"System From CSV 1"})
		csvfileWriter.writerow({"sysGuid":sysGuid,"envName":"System From CSV 2"})
		csvfile.close()
	else:
		print "Using existing CSV file for input"

	# Load CSV file	
	crEnvFile = open(csvFileName, 'r')
	# Get the field names from the header
	crEnvReader = csv.reader( crEnvFile )
	fieldnames = crEnvReader.next()
	dictReader = csv.DictReader( crEnvFile, fieldnames)
	# Create output file name with timestamp
	outfile = open('envsOut' + '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()) + '.csv', 'w')
	# TODO: remove the following line...
	dictReader = csv.DictReader( crEnvFile, fieldnames)
	# Add envGuid row to outfile
	fieldnames.append('envGuid')
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
	
	DevGuid = plutora.guidByPathAndName("lookupfields/UsedForWorkItem","Dev","value")
	ActiveGuid = plutora.guidByPathAndName("lookupfields/EnvironmentStatus","Active","value")
	for row in dictReader:
		myEnv = {
			"Vendor": "Plutora",
			"UsageWorkItemId": DevGuid,
			"EnvironmentStatusId": ActiveGuid,
			"Color": "#ffffff",
			"IsSharedEnvironment": "true"
		}
		myEnv['name']=row['envName']
		myEnv['LinkedSystemId']=row['sysGuid']
		env = plutora.api("POST", "environments", myEnv)
		envApi = "environments/" + env['id']
		print "Creating " + envApi
		row['envGuid']=env['id']
		writer.writerow(row)
	crEnvFile.close()
		
	
if False: # Set test value to True to run example
	## Delete the Environments created above by loading the CSV which includes the GUIDs to be deleted
	# Assumes there is an envGuid column
	#
	# TODO: debug why script fails if this and the above examples are set to True (each runs fine on own)
		# Loading file: envsOut20170330145538.csv
		# Traceback (most recent call last):
		  # File ".\apiFunctions.py", line 255, in <module>
			# fieldnames = delEnvReader.next()
		# StopIteration
	#
	import glob,csv
	for file in glob.glob('environments20170424231824.csv'):
		print "Loading file: " + file
		# Load CSV file	
		delEnvInfile = open(file, 'r')
		delEnvReader = csv.reader( delEnvInfile )
		
		## Capture field names from header row
		fieldnames = delEnvReader.next()
		dictReader = csv.DictReader( delEnvInfile, fieldnames)

		for row in dictReader:
			envApi = "environments/" + row['envGuid']
			print "Deleting " + envApi
			plutora.api("DELETE", envApi)
		
		delEnvInfile.close()
if False: # Set test value to True to run example
	## Set a component version
	path = {
		"environmentName": "Jenkins - DEV",
		"hostName": "jenkinsDemoDev",
		"layerType": "Application",
		"componentName": "JenkinsWebDemo"
	}
	componentGuid = plutora.getComponentId(path)
	layerData = plutora.api("GET","layers/"+componentGuid)
	layerData['version']="1.0-testApi"
	plutora.api("PUT","layers/"+componentGuid,layerData)