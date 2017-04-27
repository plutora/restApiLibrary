# Python 2.7
#
# Export Plutora objects to a CSV file
#
# python exportObjects.py --csvFile <output filepath without extension> --objectType <systems|environments> --filter <string to match>
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
	elif (objectType=="environments"):
		systems = plutora.listToDict(plutora.api("GET","systems"), "id", "name")
		useFor = plutora.listToDict(plutora.api("GET","lookupfields/UsedForWorkItem"), "id", "value")
		envStatatus = plutora.listToDict(plutora.api("GET","lookupfields/EnvironmentStatus"), "id", "value")
		layers = plutora.listToDict(plutora.api("GET","lookupfields/StackLayer"), "id", "value")

	for object in objects:
		if (filter in object['name']):
			objectResponse = plutora.api("GET",objectType+"/"+object['id'])
			if (objectType=="systems"):
				row = {
					"Name":objectResponse['name'],
					"Vendor":objectResponse['vendor'],
					"Status":objectResponse['status'],
					# TODO: handle hiearchy
					"Organization":organizations[objectResponse['organizationId']]
					# TODO: enable description... bad characters codes
					#"description":objectResponse.get('description',''),
					# "isAllowEdit":objectResponse['isAllowEdit'],
					# "inMyOrganization":objectResponse['inMyOrganization']
				}
			elif (objectType=="environments"):
				row = {
					"Name": objectResponse['name'],
					# TODO: handle description
					#"Description": objectResponse.get('description',''),
					"URL": objectResponse.get('url',''),
					"Vendor": objectResponse['vendor'],
					"LinkedSystem": systems[objectResponse['linkedSystemId']],
					"EnvironmentMgr": objectResponse.get('environmentMgr',''),
					"UsageWorkItem": useFor[objectResponse['usageWorkItemId']],
					"EnvironmentStatus": envStatatus[objectResponse['environmentStatusId']],
					"Color": objectResponse['color'],
					"IsSharedEnvironment": objectResponse['isSharedEnvironment']
				}
			print "Writing " + object['name']
			csvfileWriter.writerow(row)
	csvfile.close()

import sys, getopt

def main(argv):
	filename = ''
	objectType = ''
	usage = 'USAGE: python importObjects.py --csvFile <input filePath, no extension> --objectType <systems|environments> --filter <string to match>'
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
			if not (arg in ["systems","environments"]):
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
			



