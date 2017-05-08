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
#				 	name,vendor,status,organization,description
#	Environments:
#		Required:	*                    *      *                           *             *                 *     *
#		ID Lookup:	                            *                           *             *                                                    *
#					name,description,url,vendor,linkedSystem,environmentMgr,UsageWorkItem,EnvironmentStatus,color,isSharedEnvironment,hostName,StackLayer,componentName,version
#
#	Releases:
#		Required:	*          *            *           *        *                 *                *                 *             *            *                     *                  *
#		ID Lookup:	                        *                    *                 *                                                *            *       *
#					identifier,name,summary,ReleaseType,location,ReleaseStatusType,ReleaseRiskLevel,implementationDate,displayColor,organization,Manager,ParentRelease,plutoraReleaseType,releaseProjectType
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
			'name': row['name'],
			'description': row['description'],
			'status': row['status'],
			# TODO: handle hierarchy
			'OrganizationId': organizations[row['organization']],
			'vendor': row['vendor']
		}		
		# Does the named object exist?
		if (row['name'] in existingObjects):	# Exists
			print "System \"" + row['name']+ "\" exists, updating"
			systemGuid = existingObjects[row['name']]
			systemData['Id'] = systemGuid
			systemResponse = plutora.api("PUT", "systems/"+systemGuid, systemData)
		else:									# Does not exist
			print "System \"" + row['name']+ "\" does not exist, creating"
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
			'name': row['name'],
			'description': row['description'],
			'url': row['url'],
			'vendor': row['vendor'],
			'LinkedSystemId': systems[row['linkedSystem']],
			'environmentMgr': row['environmentMgr'],
			'UsageWorkItemId': useFor[row['UsageWorkItem']],
			'EnvironmentStatusId': envStatatus[row['EnvironmentStatus']],
			'color': row['color'],
			'isSharedEnvironment': row['isSharedEnvironment']
			# TODO: add hosts, layers and components
		}		
		# Does the named object exist?
		if (row['name'] in existingObjects):	# Exists
			print "Environment \"" + row['name']+ "\" exists, updating"
			environmentGuid = existingObjects[row['name']]
			environmentData['Id'] = environmentGuid
			environmentResponse = plutora.api("PUT", "environments/"+environmentGuid, environmentData)
		else:									# Does not exist
			print "Environment \"" + row['name']+ "\" does not exist, creating"
			environmentResponse = plutora.api("POST", "environments", environmentData)
			environmentApi = "environments/" + environmentResponse['id']
			print "Created " + environmentApi + " - " + environmentResponse['name']
			row['environmentGuid']=environmentResponse['id']
			environmentGuid = environmentResponse['id']
		 
		# Add host
		if row.get('hostName'):
			hosts(row,environmentGuid)
			
def hosts(row,environmentId):
	hostName = row['hostName']
	hostData = {
		'name': hostName,
		'EnvironmentID': environmentId
	}
	existingObjects = plutora.listToDict(plutora.api("GET","environments/"+environmentId)['hosts'], "name", "id")
	if (hostName in existingObjects):	# Exists
		print "Host \"" + hostName + "\" exists, updating"
		hostGuid = existingObjects[hostName]
		hostData['Id'] = hostGuid
		hostResponse = plutora.api("PUT", "hosts/"+hostGuid, hostData)
	else:									# Does not exist
		print "Host \"" + hostName + "\" does not exist, creating"
		hostResponse = plutora.api("POST", "hosts", hostData)
		hostApi = "hosts/" + hostResponse['id']
		print "Created " + hostApi + " - " + hostResponse['name']
		row['hostGuid']=hostResponse['id']
		hostGuid = hostResponse['id']
	

def releases(rowReader):
	existingObjects = plutora.listToDict(plutora.api("GET","releases"), "identifier", "id")
	organizations = plutora.listToDict(plutora.api("GET","organizations"), "name", "id")
	releaseTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseType"), "value", "id")
	users = plutora.api("GET","users")
	managers = plutora.listToDict(users, "userName", "id")
	releaseStatusTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseStatusType"), "value", "id")
	releaseRiskLevels = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseRiskLevel"), "value", "id")
	parentReleases = existingObjects

	for row in rowReader:
		# Common release data whether exists or not
		releaseData = {
			'identifier': row['identifier'],
			'name': row['name'],
			'summary': row['summary'],
			'ReleaseTypeId': releaseTypes[row['ReleaseType']],
			'location': row['location'] or "NA",
			'ReleaseStatusTypeId': releaseStatusTypes[row['ReleaseStatusType']],
			'ReleaseRiskLevelId': releaseRiskLevels[row['ReleaseRiskLevel']],
			'implementationDate': row['implementationDate'],
			'displayColor': row['displayColor'],
			'OrganizationId': organizations[row['organization']],
			# TODO: temporary workaround for REST required field which is not required in UI
			'ManagerId': managers.get(row['Manager'] or users[0]['userName']),
			'ParentReleaseId': parentReleases.get(row['ParentRelease']),
			'plutoraReleaseType': row['plutoraReleaseType'],
			'releaseProjectType': row['releaseProjectType']
			# TODO: Additional items
		}		
		# Does the named object exist?
		if (row['identifier'] in existingObjects):	# Exists
			print "Release \"" + row['identifier']+ "\" exists, updating"
			releaseGuid = existingObjects[row['identifier']]
			releaseData['Id'] = releaseGuid
			releaseResponse = plutora.api("PUT", "releases/"+releaseGuid, releaseData)
		else:									# Does not exist
			print "Release \"" + row['identifier']+ "\" does not exist, creating"
			releaseResponse = plutora.api("POST", "releases", releaseData)
			releaseApi = "releases/" + releaseResponse['id']
			print "Created " + releaseApi + " - " + releaseResponse['identifier']
			row['releaseGuid']=releaseResponse['id']
			
import sys, getopt

def main(argv):
	filename = ''
	objectType = ''
	usage = 'USAGE: python importObjects.py --csvFile <filePath, no extension> --objectType <systems|environments|releases>'
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
			if not (arg in ["systems","environments","releases"]):
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
	elif (objectType=="releases"):
		releases(rowReader)	



