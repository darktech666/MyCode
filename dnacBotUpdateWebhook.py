import requests   # We use Python "requests" module to do HTTP GET query
import json       # Import JSON encoder and decode module
import sys
import myVault
# import myModules
requests.packages.urllib3.disable_warnings()

runMode = input("Enter 1 for DNACenter bot or 2 for SandBoxDNA bot :")

if runMode == "1":
	bearer = myVault.botDNACenter()
elif runMode == "2":
	bearer = myVault.botSandBoxDNACenter()
else:
	print("Not valid choice!")
	sys.exit()

myticket = "Bearer " + bearer

CONTROLLER_IP = "api.ciscospark.com"
endURL = "/v1/webhooks"   # API base url

url = "https://" + CONTROLLER_IP + endURL  # + param   # API base url

header = {"Authorization": myticket, "content-type": "application/json"}

resp = requests.get(url, headers=header)

response_json = resp.json()  # Get the json-encoded content from response

newWhTargetUrl = input("New URL:")

for f in response_json["items"]:
	whId = f["id"]
	whName = f["name"]
	oldWhTargetUrl = f["targetUrl"]
	endURL = "/v1/webhooks/" + whId
	param = {"name": whName, "targetUrl": newWhTargetUrl}
	url = "https://" + CONTROLLER_IP + endURL

	requests.put(url, headers=header, json=param)

endURL = "/v1/webhooks"
url = "https://" + CONTROLLER_IP + endURL
resp = requests.get(url, headers=header)
response_json = resp.json()  # Get the json-encoded content from response
print(json.dumps(response_json, indent=4))
