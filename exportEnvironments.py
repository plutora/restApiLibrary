## Export Environments to CSV file
# TODO: Either add additionalInformation fields and hosts/layers/components or separate script
#
import plutora,csv
csvFileName = 'envExport.csv'
fieldnames = [
	"name",
	"description",
	"url",
	"vendor",
	"linkedSystem",
	"environmentMgr",
	"usageWorkItem",
	"environmentStatus",
	"color",
	"isSharedEnvironment"
]
systems = plutora.listToDict(plutora.api("GET","systems"), "id", "name")
useFor = plutora.listToDict(plutora.api("GET","lookupfields/UsedForWorkItem"), "id", "value")
envStatatus = plutora.listToDict(plutora.api("GET","lookupfields/EnvironmentStatus"), "id", "value")
print "Creating CSV file for output"
csvfile = open(csvFileName, 'w')
csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
csvfileWriter.writeheader()
environments = plutora.api("GET","environments")
for env in environments:
	environment = plutora.api("GET","environments/"+env['id'])
	row = {
		"name": environment['name'],
		"description": environment['description'],
		"url": environment['url'],
		"vendor": environment['vendor'],
		"linkedSystem": systems[environment['linkedSystemId']],
		"environmentMgr": environment['environmentMgr'],
		"usageWorkItem": useFor[environment['usageWorkItemId']],
		"environmentStatus": envStatatus[environment['environmentStatusId']],
		"color": environment['color'],
		"isSharedEnvironment": environment['isSharedEnvironment']
	}
	print "Writing Environment " + environment['name']
	csvfileWriter.writerow(row)
csvfile.close()
