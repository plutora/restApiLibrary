import plutora

dupes = [
"ALM-Test",
"Altitude-Test",
"ASM-Test",
"BACS-Test",
"Cascade-Test",
"CDM-Test",
"Cognos-Test",
"Cybertech-Test",
"Docusign-Test",
"EDI-Test",
"eGain-Test",
"Engage-Test",
"ESB-Test",
"Filestore-Test",
"iprompt-Test",
"Keyfile/file360-Test",
"MIS01-Test",
"MQ01-Test",
"PDW-Test",
"Prompt-Test",
"Quantum-Test",
"Securitisation-Test",
"TDW-Test",
"TEST-IPJOBS-Test",
"TM1-Test"
]

for dupe in dupes:
	envGuid = plutora.guidByPathAndName("environments", dupe, field="name")
	print "Deleting " + dupe + " " + envGuid
	plutora.api("DELETE","environments/"+envGuid)