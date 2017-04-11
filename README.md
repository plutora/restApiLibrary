# restApiLibrary - Plutora REST API library and samples
## Plutora REST API Python Library
The Python file [plutora.py](plutora.py) provides helper functions for creating Plutora REST API scripts.  These include:
- Read in credentials from a file
- Wrapper to make REST calls
- Transform an array response into a look up table
- Look up GUID by object path and name

## Plutora REST API Python Samples
The Python file [apiSamples.py](apiSamples.py) provides example calls that illustrate how to interact with the Plutora REST API.  These include:
- Get list of System names with GET
- Look up a system GUID by system name
- Look up a GUID by API path and object name
- Create a System and Enviroment with POST
- Change values on a System with PUT
- Delete an Enviroment with DELETE
- Create Environments from CSV file and document the results in a new CSV file with the Enviroment GUID
- Delete the Environments created above by loading the CSV which includes the GUIDs to be deleted

## Plutora REST API Primer
The file [Plutora REST API Primer.pdf](Plutora%20REST%20API%20Primer.pdf) explains in detail how to use the Plutora REST API along with some examples.  These examples are also implemented in the Python script file [primerImplementations]

## Instructions
- Create a credentials.cfg file from [credentials.cfg_template](credentials.cfg_template), adding your credentials and Plutora instance details.  Not that if you leave the password blank, you will be prompted for it at the command line.
- Create a simple test file or used the one provided
-- Add the following to a file [test.py](test.py) and run
```
import plutora
print plutora.api("GET", "me")
```
- python test.py
The script should return your email address.
