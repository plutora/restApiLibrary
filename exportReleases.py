## Export Releases to CSV file
# TODO: Either add additionalInformation fields or separate script
#
import plutora,csv,urllib
csvFileName = 'releaseExport.csv'
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
	print "Processing release " + release['name']
	row = {
		# Required
		"organization": organizations[release['organizationId']],
		"identifier": release['identifier'],
		"name": release['name'],
		"implementationDate": release['implementationDate'],
		"releaseType": releaseTypes[release['releaseTypeId']],
		"releaseRiskLevel": releaseRiskLevels[release['releaseRiskLevelId']],
		# Optional
		#"summary": None if release['summary']==None else release['summary'].replace('\n',''),
		"location": release.get('location',''),
		"releaseStatusType": releaseStatusTypes[release['releaseStatusTypeId']],
		"displayColor": release.get('displayColor',''),
		"manager": release.get('manager',''),
		"parentRelease": release.get('parentRelease',''),
		"plutoraReleaseType": release.get('plutoraReleaseType',''),
		"releaseProjectType": release.get('releaseProjectType','')
	}
	csvfileWriter.writerow(row)
csvfile.close()
