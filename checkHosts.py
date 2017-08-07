import plutora

f = open('deletedHosts.txt','r')

for host in f:
	hostGuid = host.strip()
	hostdata = plutora.api("GET","hosts/"+hostGuid)
	if hostdata=="":
		print hostGuid