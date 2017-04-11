# Python 2.7
# Delete objects created by primerImplementation.py listed in primerObjects<timestamp>.txt
#
import plutora, glob

for file in glob.glob('primerObjects*.txt'):
	print "Loading file: " + file
	# Load object list file
	with open(file) as f:
		objects = [x.strip('\n') for x in f.readlines()]
	for obj in objects[::-1]:
		print "Deleting " + obj
		plutora.api("DELETE",obj)


