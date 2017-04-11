# Python 2.7
# Solution to Plutora REST API Primer
#
import plutora

# Create a file to track all created objects so they can be easily deleted
import datetime
outfile = open('primerObjects' + '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now()) + '.txt', 'w')
# TODO: create a script to delete objects in the opposite order they were created

# Solution: Environment Creation and Modification
#   Set to False to skip this example
if True:
	# Get to root level organization portfolio
	orgGuid = plutora.api("GET", "organizations")[0]['id']
	print "orgGuid " + orgGuid

	# Get UsageWorkItemId
	uwiiGuid = plutora.guidByPathAndName("lookupfields/UsedForWorkItem", "Dev", "value")
	print "uwiiGuid " + uwiiGuid
	
	# Get Environment Status GUID for "Active"
	envStatusGuid = plutora.guidByPathAndName("lookupfields/EnvironmentStatus", "Active", "value")
	print "envStatusGuid " + envStatusGuid
	
	# Get StackLayerID for "Application"
	StackLayerID = plutora.guidByPathAndName("lookupfields/StackLayer", "Application", "value")
	print "StackLayerID " + StackLayerID
	
	# Create the System
	systemData = {
		"Name": "My System",
		"Vendor": "Plutora",
		"Status": "Active",
		"OrganizationId": orgGuid
	}
	systemResponse = plutora.api("POST", "systems", systemData)
	sysGuid=systemResponse['id']
	outfile.write("systems/" + sysGuid + "\n")
	print "sysGuid " + sysGuid

	# Create the Enviroment
	environmentData = {
		"Name": "My Environment",
		"Vendor": "Plutora",
		"Color": "#ffffff",
		"IsSharedEnvironment": "true",
		"EnvironmentStatusId": envStatusGuid,
		"UsageWorkItemId": uwiiGuid,
		"LinkedSystemId": sysGuid
	}
	environmentResponse = plutora.api("POST", "environments", environmentData)
	envGuid=environmentResponse['id']
	outfile.write("environments/" + envGuid + "\n")
	print "envGuid " + envGuid

	# Create the Host
	hostData = {
		"Name": "My Host",
		"EnvironmentID": envGuid
	}
	hostResponse = plutora.api("POST", "hosts", hostData)
	hostGuid=hostResponse['id']
	outfile.write("hosts/" + hostGuid + "\n")
	print "hostGuid " + hostGuid

	# Create the Layer
	layerData = {
		"ComponentName": "My Application",
		"Version": "1.0",
		"HostID": hostGuid,
		"EnvironmentID": envGuid,
		"StackLayerID": StackLayerID
	}
	layerResponse = plutora.api("POST", "layers", layerData)
	layerGuid=layerResponse['id']
	outfile.write("layers/" + layerGuid + "\n")
	print "layerGuid " + layerGuid

# Solution: Modify Environment and Component Fields
#   Set to False to skip this example
if True:
	# Find our Environment from amoung all those in Plutora instance
	myEnvGuid = plutora.guidByPathAndName("environments", "My Environment")
	print "myEnvGuid " + myEnvGuid
	
	# Get our Environment details
	myEnv = plutora.api("GET", "environments/" + myEnvGuid)
	myEnvName = myEnv['name']
	print "myEnvName " + myEnvName
	
	# Add a description
	myEnv['description']="Here is the description of My Environment"
	myEnvResponse=plutora.api("PUT", "environments/" + myEnvGuid, myEnv)
	
	# Find the component version to adjust, assume only one host and one layer
	myLayerGuid = myEnv['hosts'][0]['layers'][0]['id']
	print "myLayerGuid " + myLayerGuid
	
	# Set the new value in the component layer
	myLayerData=plutora.api("GET", "layers/" + myLayerGuid)
	myLayerData['version']="2.0"
	myLayerResponse=plutora.api("PUT", "layers/" + myLayerGuid, myLayerData)
	
# Solution: Create an Environment Group with two connected Environments
#   Set to False to skip this example
#   This section relies on the previous for some variables
if True:
	# Create the System
	systemData = {
		"Name": "My second System",
		"Vendor": "Plutora",
		"Status": "Active",
		"OrganizationId": orgGuid
	}
	systemResponse = plutora.api("POST", "systems", systemData)
	secondSysGuid=systemResponse['id']
	outfile.write("systems/" + secondSysGuid + "\n")
	print "secondSysGuid " + secondSysGuid

	# Create the Enviroment
	environmentData = {
		"Name": "My second Environment",
		"Vendor": "Plutora",
		"Color": "#ffffff",
		"IsSharedEnvironment": "true",
		"EnvironmentStatusId": envStatusGuid,
		"UsageWorkItemId": uwiiGuid,
		"LinkedSystemId": secondSysGuid
	}
	environmentResponse = plutora.api("POST", "environments", environmentData)
	secondEnvGuid=environmentResponse['id']
	outfile.write("environments/" + secondEnvGuid + "\n")
	print "secondEnvGuid " + secondEnvGuid
	
	# Create the Environment Group
	firstEnvGuid = plutora.guidByPathAndName("environments", "My Environment")
	envGroupData = {
		"Name": "My Environment Group",
		"Description": "My Environment Group description",
		"Color": "#ffffff",
		"EnvironmentIDs": [
			firstEnvGuid,
			secondEnvGuid
		]
	}
	envGroupResponse = plutora.api("POST", "environmentgroups", envGroupData)
	envGroupGuid = envGroupResponse['id']
	outfile.write("environmentgroups/" + envGroupGuid + "\n")
	print "envGroupGuid " + envGroupGuid
	
	# Create HTTPS Environment Connection
	httpsGuid = plutora.guidByPathAndName("lookupfields/EnvironmentMapConnectivityType", "HTTPS", "value") 
	connectiviesData = {
		"connectivityType": httpsGuid,
		"direction": "InAndOut",
		"environmentGroup": envGroupGuid,
		"source": firstEnvGuid,
		"target": secondEnvGuid
	}
	connectiviesResponse=plutora.api("POST", "connectivities", connectiviesData)
	# POST connectivities not returning anything, 
	# connGuid = connectiviesResponse['id']
	# outfile.write("connectivities/" + connGuid + "\n")
	# print "connGuid " + connGuid
	
outfile.close()

