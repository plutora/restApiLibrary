import requests
import os
import os.path
import xmltodict
import sys

loginHash = {
    'client_id': 'D4MP726BR4JEZLWRQX7RMI7IAU',
    'client_secret': 'FKBNBWPZ4YXUPHZNGN5XV7TSSM',
    'grant_type': 'password',
    'username': 'nicholas.gulrajani@plutora.com',
    'password': 'plutora1234'
}

fileName = sys.argv[1]

if not os.path.exists(os.path.join(os.getcwd(),fileName)):
    print ("File does not exist.. exiting")
    sys.exit(-1)

with open(os.path.join(os.getcwd(), fileName)) as fd:
    doc = xmltodict.parse(fd.read())
    
    name = doc['changes']['@name']
    changePriority = doc['changes']['ChangePriority']
    changeStatus = doc['changes']['ChangeStatus']
    changeType = doc['changes']['ChangeType']
    changeDeliveryRisk = doc['changes']['ChangeDeliveryRisk']
    changeTheme = doc['changes']['ChangeTheme']
    raisedByUser = doc['changes']['RaisedByUser']
    organization = doc['changes']['Organization']

# Function to filter out the names
def names(name):
    return name['value']

res = requests.post('https://usoauth.plutora.com/oauth/token', data=loginHash, headers= { 'Content-Type': 'application/x-www-form-urlencoded'})
auth_token = None
if res.status_code == 200:
    auth_token = str(res.json()['access_token'])
else:
    print ("Error logging in , pls check credentials")
    sys.exit(-1)
    
if not auth_token:
    print ("Error authenticating.. Exiting....")
    sys.exit(-1)

auth_header = { 'Authorization': 'bearer %s' %(auth_token,) }

# Verify that all is okay by pritning the email associated with user
res = requests.get('https://usapi.plutora.com/me', headers=auth_header)
print (res.text)

# Get the Keys for "Changes" POST request
changePriorityResponse = requests.get('https://usapi.plutora.com/lookupfields/ChangePriority', headers=auth_header)
if changePriorityResponse.status_code != 200:
    print ("Error getting Change priorities")
    sys.exit(-1)

changePriorities = changePriorityResponse.json()

changePriorityVal = [changePriorityVal for changePriorityVal in changePriorities if changePriorityVal['value'] == changePriority]
if len(changePriorityVal) == 0:
    print ("Cannot find Change Priority with %s. Has to be one of %s") %(changePriority, ','.join(map(names, changePriorities)))
    sys.exit(-1)
else:
    changePriorityId = changePriorityVal[0]['id']

changeStatusResponse = requests.get('https://usapi.plutora.com/lookupfields/ChangeStatus', headers=auth_header)
if changeStatusResponse.status_code != 200:
    print ("Error getting Change status")
    sys.exit(-1)

changeStatuses = changeStatusResponse.json()

changeStatusVal = [changeStatusVal for changeStatusVal in changeStatuses if changeStatusVal['value'] == changeStatus]
if len(changeStatusVal) == 0:
    print ("Cannot find Change Status with %s. Has to be one of %s") %(changeStatus, ','.join(map(names, changeStatuses)))
    sys.exit(-1)
else:
    changeStatusId = changeStatusVal[0]['id']

changeTypeResponse = requests.get('https://usapi.plutora.com/lookupfields/ChangeType', headers=auth_header)
if changeStatusResponse.status_code != 200:
    print ("Error getting Change Type")
    sys.exit(-1)

changeTypes = changeTypeResponse.json()

changeTypeVal = [changeTypeVal for changeTypeVal in changeTypes if changeTypeVal['value'] == changeType]
if len(changeTypeVal) == 0:
    print ("Cannot find Change Type with %s. Has to be one of %s") %(changeType, ','.join(map(names, changeTypes)))
    sys.exit(-1)
else:
    changeTypeId = changeTypeVal[0]['id']

changeDeliveryRiskResponse = requests.get('https://usapi.plutora.com/lookupfields/ChangeDeliveryRisk', headers=auth_header)
if changeDeliveryRiskResponse.status_code != 200:
    print ("Error getting Change Delivery Risk")
    sys.exit(-1)

changeDeliveryRisks  = changeDeliveryRiskResponse.json()

changeDeliveryRiskVal = [changeDeliveryRiskVal for changeDeliveryRiskVal in changeDeliveryRisks if changeDeliveryRiskVal['value'] == changeDeliveryRisk]
if len(changeDeliveryRiskVal) == 0:
    print ("Cannot find Change Delivery Risk with %s. Has to be one of %s") %(changeType, ','.join(map(names, changeDeliveryRisks)))
    sys.exit(-1)
else:
    changeDeliveryRiskId = changeDeliveryRiskVal[0]['id']

changeThemesResponse = requests.get('https://usapi.plutora.com/lookupfields/ChangeTheme', headers=auth_header)
if changeThemesResponse.status_code != 200:
    print ("Error getting Change Themes")
    sys.exit(-1)

changeThemes = changeThemesResponse.json()

changeThemesVal = [changeThemesVal for changeThemesVal in changeThemes if changeThemesVal['value'] == changeTheme]
if len(changeThemesVal) == 0:
    print ("Cannot find Change Theme with %s. Has to be one of %s") %(changeType, ','.join(map(names, changeThemes)))
    sys.exit(-1)
else:
    changeThemeId = changeThemesVal[0]['id']

usersResponse = requests.get('https://usapi.plutora.com/users', headers=auth_header)
if usersResponse.status_code != 200:
    print ("Error getting Users")
    sys.exit(-1)

users = usersResponse.json()
usersVal = [usersVal for usersVal in users if usersVal['userName'] == raisedByUser]
if len(usersVal) == 0:
    print ("Cannot find User with %s. ") %(raisedByUser,)
    sys.exit(-1)
else:
    userId = usersVal[0]['id']

orgResponse = requests.get('https://usapi.plutora.com/organizations', headers=auth_header)
if orgResponse.status_code != 200:
    print ("Error getting Organizations")
    sys.exit(-1)

organizations = orgResponse.json()
orgVal = [orgVal for orgVal in organizations if orgVal['name'] == organization]
if len(orgVal) == 0:
    print ("Cannot find Organization with %s. ") %(organization,)
    sys.exit(-1)
else:
    orgId = orgVal[0]['id']

changeDict = {
    "Name": str(name),
    "ChangePriorityId": str(changePriorityId),
    "ChangeStatusId": str(changeStatusId),
    "RaisedById": str(userId),
    "OrganizationId": str(orgId),
    "ChangeTypeId": str(changeTypeId),
    "ChangeDeliveryRiskId": str(changeDeliveryRiskId),
    "ChangeThemeId": str(changeThemeId)
}

changeHeaders = {
    'Authorization': 'bearer %s' %(auth_token,) 
}
res = requests.post('https://usapi.plutora.com/changes', data=changeDict, headers=changeHeaders)
if res.status_code == 201:
    print (res.text)
    print ("Change created")
else:
    print ("Error in posting changes")
