# Python 2.7
#
import os
environment = "Jenkins - DEV" 
version =  "2.0-" + os.environ['BUILD_NUMBER']

import sys
sys.path.append("/home/ec2-user/restApiLibrary")
import plutora
from optparse import OptionParser

def updateVersion(version,path):
	componentGuid = plutora.getComponentId(path)
	layerData = plutora.api("GET","layers/"+componentGuid)
	layerData['version']=version
	plutora.api("PUT","layers/"+componentGuid,layerData)

# Create path to the component to be updated
path = {
	"environmentName": environment,
	"hostName": "jenkinsDemoDev",
	"layerType": "Application",
	"componentName": "JenkinsWebDemo"
}

updateVersion(version,path)