# Python 2.7
#
# USAGE: python JenkinsDemoUpdateVersion.py <version value> <phase: DEV|QA|UAT>
#
import plutora
from optparse import OptionParser

def updateVersion(version,path):
	componentGuid = plutora.getComponentVersion(path)
	layerData = plutora.api("GET","layers/"+componentGuid)
	layerData['version']=version
	plutora.api("PUT","layers/"+componentGuid,layerData)

# Get command line arguments
parser = OptionParser()
(options, args) = parser.parse_args()
version = args[0]
phase = args[1]

# Create path to the component to be updated
path = {
	"environmentName": "Jenkins - " + phase,
	"hostName": "jenkinsDemoDev",
	"layerType": "Application",
	"componentName": "JenkinsWebDemo"
}

updateVersion(version,path)