import plutora

candidates = {
	"BACS",
	"4Series",
	"ALM",
	"ALTITUDE",
	"Batch Jobs",
	"Biztalk",
	"Business Objects",
	"CBF",
	"CBL",
	"CDM",
	"Clarity",
	"Cognos",
	"CRM",
	"Cybertech",
	"Data Warehouse",
	"Database",
	"Docusign",
	"EDI",
	"eGain",
	"Engage",
	"ENGAGE",
	"Fileserver",
	"FTP",
	"iprompt",
	"Keyfile/file360",
	"MIS01",
	"Oracle",
	"Payments",
	"Quantum",
	"SFS",
	"SSRS",
	"TDW",
	"Terminal",
	"Testing",
	"Web"
}

systems = plutora.api("GET", "systems")

for system in systems:
	found = False
	for candidate in candidates:
		if system['name']==candidate:
			print candidate + " found"
			found = True
			#break
	if not found:
		print candidate + " not found"
	