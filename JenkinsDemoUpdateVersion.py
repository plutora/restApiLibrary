import plutora
from optparse import OptionParser

def updateVersion(version,phase):
	devGuid = plutora.guidByPathAndName("environments", "Jenkins demo - " + phase, field="name")
	devData = plutora.api("GET","environments/"+devGuid)
	layerGuid = devData['hosts'][0]['layers'][0]['id']
	layerData = plutora.api("GET","layers/"+layerGuid)
	layerData['version']=version
	plutora.api("PUT","layers/"+layerGuid,layerData)
	
parser = OptionParser()
(options, args) = parser.parse_args()
version = args[0]
phase = args[1]
updateVersion(version,phase)