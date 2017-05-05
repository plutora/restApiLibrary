# Python 2.7
#
# USAGE: python JenkinsDemoUpdateVersion.py <version value> <phase: DEV|QA|UAT>
#
import plutora
from optparse import OptionParser

def updateVersion(version,environment):
	envGuid = plutora.guidByPathAndName("environments", environment, field="name")
	envData = plutora.api("GET","environments/"+envGuid)
	layerGuid = envData['hosts'][0]['layers'][0]['id']
	layerData = plutora.api("GET","layers/"+layerGuid)
	layerData['version']=version
	plutora.api("PUT","layers/"+layerGuid,layerData)
	
parser = OptionParser()
(options, args) = parser.parse_args()
version = args[0]
phase = args[1]
updateVersion(version,"Jenkins - " + phase)