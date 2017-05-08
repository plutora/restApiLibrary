# Python 2.7
#
# Export Plutora objects to a CSV file
#
# python exportObjects.py --csvFile <output filepath without extension> --objectType <systems|environments|releases> --filter <string to match>
# TODO: add Releases, and remaining objects
#
#

def exportObjects(filename,objectType,filter):
	import plutora,csv
	fieldnames = []
	for column in plutora.objectFields[objectType]:
		fieldnames.append(column['name'])
	print "Creating CSV file for output"
	csvfile = open(filename + ".csv", 'w')
	csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
	csvfileWriter.writeheader()
	objects = plutora.api("GET",objectType)
	if (objectType=="systems"):
		organizations = plutora.listToDict(plutora.api("GET","organizations"), "id", "name")
		filterKey="name"
	elif (objectType=="environments"):
		systems = plutora.listToDict(plutora.api("GET","systems"), "id", "name")
		useFor = plutora.listToDict(plutora.api("GET","lookupfields/UsedForWorkItem"), "id", "value")
		envStatatus = plutora.listToDict(plutora.api("GET","lookupfields/EnvironmentStatus"), "id", "value")
		layers = plutora.listToDict(plutora.api("GET","lookupfields/StackLayer"), "id", "value")
		filterKey="name"
	elif (objectType=="releases"):
		organizations = plutora.listToDict(plutora.api("GET","organizations"), "id", "name")
		releaseTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseType"), "id", "value")
		releaseStatusTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseStatusType"), "id", "value")
		releaseRiskLevels = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseRiskLevel"), "id", "value")
		parentReleases = plutora.listToDict(objects, "id", "identifier")
		managers = plutora.listToDict(plutora.api("GET","users"), "id", "userName")
		filterKey="identifier"
	else:
		print "Invalid object type"
		exit(10)
		
	for object in objects:
		if ((filter in object[filterKey]) or (filter=="")):
			objectResponse = plutora.api("GET",objectType+"/"+object['id'])
			if (objectType=="systems"):
				row = {
					"name":objectResponse['name'],
					"vendor":objectResponse['vendor'],
					"status":objectResponse['status'],
					# TODO: handle hiearchy
					"organization":organizations[objectResponse['organizationId']]
					# TODO: enable description... bad characters codes
					#"description":objectResponse.get('description',''),
					# "isAllowEdit":objectResponse['isAllowEdit'],
					# "inMyOrganization":objectResponse['inMyOrganization']
				}
			elif (objectType=="environments"):
				row = {
					"name": objectResponse['name'],
					# TODO: handle description
					#"description": objectResponse.get('description',''),
					"url": objectResponse.get('url',''),
					"vendor": objectResponse['vendor'],
					"linkedSystem": systems[objectResponse['linkedSystemId']],
					"environmentMgr": objectResponse.get('environmentMgr',''),
					"UsageWorkItem": useFor[objectResponse['usageWorkItemId']],
					"EnvironmentStatus": envStatatus[objectResponse['environmentStatusId']],
					"color": objectResponse['color'],
					"isSharedEnvironment": objectResponse['isSharedEnvironment']
				}
			elif (objectType=="releases"):
				row = {
					"identifier": objectResponse['identifier'],
					"name": objectResponse['name'],
					# TODO: handle summary
					#"summary": objectResponse.get('summary',''),
					"ReleaseType": releaseTypes[objectResponse['releaseTypeId']],
					"location": objectResponse['location'],
					"ReleaseStatusType": releaseStatusTypes[objectResponse['releaseStatusTypeId']],
					"ReleaseRiskLevel": releaseRiskLevels[objectResponse['releaseRiskLevelId']],
					"implementationDate": objectResponse['implementationDate'],
					"displayColor": objectResponse['displayColor'],
					"organization": organizations[objectResponse['organizationId']],
					"Manager": managers.get(objectResponse['managerId']),
					"ParentRelease": parentReleases.get(objectResponse['parentReleaseId']),
					"plutoraReleaseType": objectResponse['plutoraReleaseType'],
					"releaseProjectType": objectResponse['releaseProjectType']
				}
			print "Writing " + object[filterKey]
			csvfileWriter.writerow(row)
	csvfile.close()

import sys, getopt

def main(argv):
	filename = ''
	objectType = ''
	filter = ''
	usage = 'USAGE: python importObjects.py --csvFile <output filePath, no extension> --objectType <systems|environments|releases> --filter <string to match>'
	try:
		opts, args = getopt.getopt(argv,"hf:t:m:",["csvFile=","objectType=","filter="])
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
		elif opt in ("-m", "--filter"):
			filter = arg
		else:
			print usage
			sys.exit(4)
	print 'Output file is "', filename + '.csv"'
	print 'Object type is "', objectType + '"'
	print 'Filter is "', filter + '"'
	return filename,objectType,filter

# Only run from the command line
if __name__ == "__main__":
	filename,objectType,filter = main(sys.argv[1:])
	exportObjects(filename,objectType,filter)
			



