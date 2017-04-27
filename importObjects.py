# Python 2.7
#
# Import new or update existing Plutora objects via CSV file
#
# python importObjects.py --csvFile <filepath without extension> --objectType <systems|environments>
# TODO: add Releases, and remaining objects
#
# Columns
#	Systems:
#		Required:	*    *      *      *
#		ID Lookup:	                   *
#				 	Name,Vendor,Status,Organization,Description
#	Environments:
#		Required:	*                    *      *                           *             *                 *     *
#		ID Lookup:	                            *                           *             *                                                    *
#					Name,Description,URL,Vendor,LinkedSystem,EnvironmentMgr,UsageWorkItem,EnvironmentStatus,Color,IsSharedEnvironment,hostName,StackLayer,StackLayerType,ComponentName,Version
#
import plutora

def getRows(fileName, requiredFieldNames):
	# 1. Load CVS file
	# 2. Verify that all fields columns are present
	# 3. Return row reader object
	#
	# Load CSV file	
	import os.path,csv,datetime
	csvFileName = fileName
	inFileHandle = open(csvFileName + '.csv', 'r')
	# Get the field names from the header
	crHostReader = csv.reader( inFileHandle )
	fieldnames = crHostReader.next()
	# Verify all fields present
	for field in requiredFieldNames:
		if not field['name'] in fieldnames:
			print "\"" + field['name'] + "\" column missing from file \"" + fileName + ".csv\""
	rowReader = csv.DictReader( inFileHandle, fieldnames)
	return rowReader

def systems(rowReader):
	existingObjects = plutora.listToDict(plutora.api("GET","systems"), "name", "id")
	organizations = plutora.listToDict(plutora.api("GET","organizations"), "name", "id")
	for row in rowReader:
		# TODO: Validate fields, status Active or Inactive only
		# Common system data whether exists or not
		systemData = {
			'Name': row['Name'],
			'Description': row['Description'],
			'Status': row['Status'],
			# TODO: handle hierarchy
			'OrganizationId': organizations[row['Organization']],
			'Vendor': row['Vendor']
		}		
		# Does the named object exist?
		if (row['Name'] in existingObjects):	# Exists
			print "\"" + row['Name']+ "\" exists, updating"
			systemGuid = existingObjects[row['Name']]
			systemData['Id'] = systemGuid
			systemResponse = plutora.api("PUT", "systems/"+systemGuid, systemData)
		else:									# Does not exist
			print "\"" + row['Name']+ "\" does not exist, creating"
			systemResponse = plutora.api("POST", "systems", systemData)
			systemApi = "systems/" + systemResponse['id']
			print "Created " + systemApi + " - " + systemResponse['name']
			row['systemGuid']=systemResponse['id']

def environments(rowReader):
	existingObjects = plutora.listToDict(plutora.api("GET","environments"), "name", "id")
	systems = plutora.listToDict(plutora.api("GET","systems"), "name", "id")
	useFor = plutora.listToDict(plutora.api("GET","lookupfields/UsedForWorkItem"), "value", "id")
	envStatatus = plutora.listToDict(plutora.api("GET","lookupfields/EnvironmentStatus"), "value", "id")
	layers = plutora.listToDict(plutora.api("GET","lookupfields/StackLayer"), "value", "id")
	for row in rowReader:
		# Common environment data whether exists or not
		environmentData = {
			'Name': row['Name'],
			'Description': row['Description'],
			'URL': row['URL'],
			'Vendor': row['Vendor'],
			'LinkedSystemId': systems[row['LinkedSystem']],
			'EnvironmentMgr': row['EnvironmentMgr'],
			'UsageWorkItemId': useFor[row['UsageWorkItem']],
			'EnvironmentStatusId': envStatatus[row['EnvironmentStatus']],
			'Color': row['Color'],
			'IsSharedEnvironment': row['IsSharedEnvironment']
			# TODO: add hosts, layers and components
		}		
		# Does the named object exist?
		if (row['Name'] in existingObjects):	# Exists
			print "\"" + row['Name']+ "\" exists, updating"
			environmentGuid = existingObjects[row['Name']]
			environmentData['Id'] = environmentGuid
			environmentResponse = plutora.api("PUT", "environments/"+environmentGuid, environmentData)
		else:									# Does not exist
			print "\"" + row['Name']+ "\" does not exist, creating"
			environmentResponse = plutora.api("POST", "environments", environmentData)
			environmentApi = "environments/" + environmentResponse['id']
			print "Created " + environmentApi + " - " + environmentResponse['name']
			row['environmentGuid']=environmentResponse['id']			
			
import sys, getopt

def main(argv):
	filename = ''
	objectType = ''
	usage = 'USAGE: python importObjects.py --csvFile <filePath, no extension> --objectType <systems|environments>'
	try:
		opts, args = getopt.getopt(argv,"hf:t:",["csvFile=","objectType="])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print usage
			sys.exit()
		elif opt in ("-f", "--csvFile"):
			filename = arg
		elif opt in ("-t", "--objectType"):
			objectType = arg
			if not (arg in ["systems","environments"]):
				print "Bad object type"
				print usage
				sys.exit(3)
		else:
			print usage
			sys.exit(4)
	print 'Input file is "', filename + '.csv"'
	print 'Object type is "', objectType + '"'
	return filename,objectType

# Only run from the command line
if __name__ == "__main__":
	filename,objectType = main(sys.argv[1:])
	rowReader = getRows(filename,plutora.objectFields[objectType])
	if (objectType=="systems"):
		systems(rowReader)
	elif (objectType=="environments"):
		environments(rowReader)
			



