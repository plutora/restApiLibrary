# python 2.7
# Create Plutora Release Activities from Jira Tasks
# To use, you'll need to provide a valid Jira crendials file (jira.cfg): 
#	{
#		"username":"JiraLoginName",
#		"password":"JiraLoginPassword"
#	}
# and a credentials.cfg file for the Plutor login:
#	{
#	  "urls":{
#		"authUrl":"https://usoauth.plutora.com/",
#		"baseUrl":"https://usapi.plutora.com/"
#	  },
#	  "credentials": {
#		"client_id":"XXXXXXXXXXXXXXXXXXXXXXXXXX",
#		"client_secret":"YYYYYYYYYYYYYYYYYYYYYYYYYY",
#		"username":"PlutoraLoginName",
#		"password":"PlutoraLoginPassword"
#		}
#	}
# Where usoath and usapi should be replaced by ukoath and ukapi is you're
# using a UK-based Plutora instance, and auoath and uaapi if in Asia.
# Set a valid Release name and one of its Phase names below:
releaseName = 'Test add issues from Jira'
releasePhase = "DEV"
# Identify an existing Release stakeholder to assign the Activities, for example:
releaseStakeholder = 'greg.maxey@plutora.com'
# Create a Jira filter to find the desired tasks, for example:
jql_str = 'type = task and duedate>"2017-01-01"'

#---------------END of instructions--------------------------------------

# pip install jira
from jira import JIRA
import re
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'restApiLibrary'))
# github.com/plutora/restApiLibrary
import plutora
import json

# Jira Credentials - load from jira.cfg
with open("jira.cfg") as data_file:
	jiraCfg = json.load(data_file)
j_url = jiraCfg["url"]
j_user = jiraCfg["username"]
j_password = jiraCfg["password"]

# Login to Plutora Jira instance
jira = JIRA(server=j_url,basic_auth=(j_user,j_password))

# Select Release to apply the tasks/Activities to
releaseId = plutora.guidByPathAndName('releases',releaseName)
# Select target Release Phase for the Activities
DEV_phaseId = plutora.guidByPathAndName('workitemnames/phases',releasePhase)

# Retrieve Jira tasks
tasks = jira.search_issues(jql_str, startAt=0, maxResults=10, validate_query=True,
              fields=None, expand=None, json_result=None)
print "Found %d Jira tasks." % len(tasks)
# For each Jira task found
for task in tasks:
	print "Processing Jira task %s" % jira.issue(task.key)
	taskHandle = jira.issue(task.id)
	Title = taskHandle.raw['fields']['summary']
	Description = "Jira task %s" % jira.issue(task.key)
	EndDate = taskHandle.raw['fields']['duedate']
	# Only create Activities with due dates
	if (EndDate==None):
		break
	#print "%sT00:00:00" % EndDate

	activity = {
		'Title': Title,
		'Description': Description,
		'ActivityDependencyType': 'None',
		'Type': 'Activity',
		'Status': 'NotStarted',
		'AssignedToID': plutora.guidByPathAndName('users',releaseStakeholder,field="userName"),
		'AssignedWorkItemID': plutora.guidByPathAndName("releases/%s/phases" % releaseId, DEV_phaseId, field="workItemNameID"), # Phase
		'EndDate': "%sT00:00:00" % EndDate
	}
	plutora.api('POST',"releases/%s/activities" % releaseId ,data=activity)
