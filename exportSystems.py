## Export Systems to CSV file
# TODO: Either add additionalInformation fields or separate script
#
import plutora,csv
csvFileName = 'sysExport.csv'
fieldnames = [
	"name",
	"vendor",
	"status",
	"organization",
	"description",
	"isAllowEdit",
	"inMyOrganization"
]
organizations = plutora.listToDict(plutora.api("GET","organizations"), "id", "name")
print "Creating CSV file for output"
csvfile = open(csvFileName, 'w')
csvfileWriter = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
csvfileWriter.writeheader()
systems = plutora.api("GET","systems")
for sys in systems:
	system = plutora.api("GET","systems/"+sys['id'])
	row = {
		"name":system['name'],
		"vendor":system['vendor'],
		"status":system['status'],
		"organization":organizations[system['organizationId']],
		#"description":system.get('description',''),
		"isAllowEdit":system['isAllowEdit'],
		"inMyOrganization":system['inMyOrganization']
	}
	print "Writing System " + system['name']
	csvfileWriter.writerow(row)
csvfile.close()
