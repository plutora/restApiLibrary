import plutora

environments = plutora.api("GET", "environments")
for environment in environments:
	if ("API" in environment['name']):
		print plutora.api("DELETE", "environments/" + environment['id'])
