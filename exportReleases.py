## Export Releases to CSV file
# TODO: Either add additionalInformation fields or separate script
#
import plutora,csv
csvFileName = 'sysExport.csv'
fieldnames = [
	"identifier",
	"name",
	"summary",
	"releaseType",
	"releaseType",
	"location",
	"releaseStatusType",
	"releaseRiskLevel",
	"releaseRiskLevel",
	"implementationDate",
	"displayColor",
	"organization",
	"manager",
	"parentRelease",
	"plutoraReleaseType",
	"releaseProjectType"
]
organizations = plutora.listToDict(plutora.api("GET","organizations"), "id", "name")
releaseTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseType"), "id", "value")
releaseStatusTypes = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseStatusType"), "id", "value")
releaseRiskLevels = plutora.listToDict(plutora.api("GET","lookupfields/ReleaseRiskLevel"), "id", "value")
parentReleases = plutora.listToDict(plutora.api("GET","releases"), "id", "name")
managers = plutora.listToDict(plutora.api("GET","users"), "id", "userName")
print "Creating CSV file for output"
csvfile = open(csvFileName, 'w')
csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
csvfileWriter.writeheader()
releases = plutora.api("GET","releases")
for rel in releases:
	release = plutora.api("GET","releases/"+rel['id'])
	row = {
		"identifier": release['identifier'],
		"name": release['name'],
		"summary": release['summary'],
		"releaseType": releaseTypes[release['releaseTypeId']],
		"releaseType": release['releaseType'],
		"location": release['location'],
		"releaseStatusType": releaseStatusTypes[release['releaseStatusTypeId']],
		"releaseRiskLevel": releaseRiskLevels[release['releaseRiskLevelId']],
		"implementationDate": release['implementationDate'],
		"displayColor": release['displayColor'],
		"organization": organizations[release['organizationId']],
		#"manager": managers[release['managerId']],
		#"parentRelease": parentReleases[release['parentReleaseId']],
		"plutoraReleaseType": release['plutoraReleaseType'],
		"releaseProjectType": release['releaseProjectType']
	}
	print "Writing release " + release['name']
	csvfileWriter.writerow(row)
csvfile.close()
