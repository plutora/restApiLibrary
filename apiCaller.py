# Python 2.7
# apiCaller.py
#
# Description: Command line tool to issue Plutora REST API Calls
#
# Usage: python apiCaller.py <verb> <path>
# Example: python apiCaller.py GET systems
#
import plutora,sys,json
print json.dumps(plutora.api(sys.argv[1],sys.argv[2]),indent=4)