# restApiLibrary - Plutora REST API library and samples
Python 2.7 code to help users develop scripts to load data and create objects in Plutora. See [Plutora REST API Documentation](http://help.plutora.com/knowledge-base/visualize-plutoras-api-with-swagger/) for additional details.
## Plutora REST API Python Library
The Python script [plutora.py](plutora.py) provides helper functions for creating Plutora REST API scripts.  These include:
- Read in credentials from a file
- getAccessToken(): return access token
- api(verb, api, data=""): Wrapper to make REST calls
- listToDict(list, key, value): Transform an array response into a look up table
- guidByPathAndName(path, name, field="name"): Look up GUID by object path and name
- getComponentId(path): Return the layer GUID where a component is defined.  Useful for getting and setting component versions.
- objectFields: Data structure schema for Plutora objects

## Plutora REST API Python Samples
The Python script [apiSamples.py](apiSamples.py) provides example calls that illustrate how to interact with the Plutora REST API.  These include:
- Get list of System names with GET
- Look up a system GUID by system name
- Look up a GUID by API path and object name
- Create a System and Enviroment with POST
- Change values on a System with PUT
- Delete an Enviroment with DELETE
- Create Environments from CSV file and document the results in a new CSV file with the Enviroment GUID
- Delete the Environments created above by loading the CSV which includes the GUIDs to be deleted
- Set a component version

## Instructions
- Create a **credentials.cfg** file from [credentials.cfg_template](credentials.cfg_template), adding your credentials and Plutora instance details.  Not that if you leave the password blank, you will be prompted for it at the command line.
- Create a simple test script or used [the one provided](test.py) by adding the following to a file **test.py**:
```
import plutora
print plutora.api("GET", "me")
```
- And run
```python test.py```
- The script should return your email address.
- You can also run ```python apiSamples.py```, but note that there are ```if False:``` flags set on all the examples, so each will be skipped unless its flag is changed to ```if True:``` 


## Plutora REST API Primer
The file [Plutora REST API Primer.pdf](Plutora%20REST%20API%20Primer.pdf) explains in detail how to use the Plutora REST API along with some examples.  These examples are also implemented in the Python script [primerImplementations.py](primerImplementations.py)

## Command Line Examples

### Command line Plutora REST API caller
The Python script [apiCaller.py](apiCaller.py) can be used to issue REST calls from the command line.  ```python apiCaller.py GET systems``` will return a JSON list of the the Systems in the users Plutora instance.

### Generate api_key for Plutora Swagger REST API Documentation
The Plutora Swagger REST API Documentation requires an api_key to run API commands.  The Python script [getAccessToken.py](getAccessToken.py) can be used to generte an api_key, ```python getAccessToken.py``` will return a token value that can be used in Swagger.

### Export Examples
Python script illustrates how to export various Plutora objects to CSV files.  These are very much works-in-progress with limited testing.
- [exportObjects.py](exportObjects.py) - Export Plutora objects from CSV files (currently supports Systems, Environments and Releases)

### Import Examples
Python script illustrates how to import various Plutora objects to CSV files.  These are very much works-in-progress with limited testing.
- [importObjects.py](importObjects.py) - Import Plutora objects from CSV files (currently supports Systems, Environments and Releases)
