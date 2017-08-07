import plutora,sys,json

releases = plutora.api("GET", "releases")
for rel in releases:
	release = plutora.api("GET","releases/"+rel['id'])
	print "Processing release " + release['name']