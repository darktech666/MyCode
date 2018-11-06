import requests   # We use Python "requests" module to do HTTP GET query
import json       # Import JSON encoder and decode module
import myModules
import myVault
requests.packages.urllib3.disable_warnings()

myticket = "Bearer " + myVault.wbxTeamsToken()

CONTROLLER_IP = "api.ciscospark.com"
endURL = "/v1/rooms"   # API base url
param = "?max=1000"

url = "https://" + CONTROLLER_IP + endURL + param   # API base url

header = {"Authorization": myticket, "content-type": "application/json"}

resp = requests.get(url, headers=header)

response_json = resp.json()  # Get the json-encoded content from response

print("Status: ", resp.status_code)    # This is the http request status
print("Description: ", myModules.errorCode(resp.status_code))
print("\n\r\r    Sous la forme json:\r", json.dumps(response_json, indent=4))
