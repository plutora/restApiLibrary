# Python 2.7
# getAccessToken.py
#
# Description: Return a current access_token for use in Plutora Swagger interface
#
# Usage: python getAccessToken.py
#
import plutora
print "bearer " + plutora.getAccessToken()