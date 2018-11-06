import requests   # We use Python "requests" module to do HTTP GET query
# import json       # Import JSON encoder and decode module
import myModules
import myVault

requests.packages.urllib3.disable_warnings()

roomId = input("What is the room ID : ")
filename = input("What is the filename : ")

myticket = "Bearer " + myVault.wbxTeamsToken()

CONTROLLER_IP = "api.ciscospark.com"
endURL = "/v1/messages"   # API base url
param = "?max=1000000000&roomId=" + roomId

url = "https://" + CONTROLLER_IP + endURL + param   # API base url

header = {"Authorization": myticket, "content-type": "application/json"}

resp = requests.get(url, headers=header)

response_json = resp.json()  # Get the json-encoded content from response

endURL2 = "/v1/memberships"   # API base url
param2 = "?max=1000&roomId=" + roomId

url2 = "https://" + CONTROLLER_IP + endURL2 + param2   # API base url

header2 = {"Authorization": myticket, "content-type": "application/json"}

resp2 = requests.get(url2, headers=header2)

response_json2 = resp2.json()  # Get the json-encoded content from response
# print("\n\r\r    Sous la forme json:\r", json.dumps(response_json2, indent=4))

print("Status: ", resp.status_code)    # This is the http request status
print("Description: ", myModules.errorCode(resp.status_code))

file = open(filename, "w")

for f in reversed(response_json["items"]):
	if "text" in f:
		if f["text"] != "":
			# for i in response_json2["items"]:
			# 	if i["personEmail"] == f["personEmail"]:
			# 		displayName = i["personDisplayName"]
			# file.write(displayName + " (" + f["personEmail"] + ") " + f["created"] + "\n")
			file.write(f["personEmail"] + " " + f["created"] + "\n")
			file.write(f["text"] + "\n")
			file.write("----------------------------------------------------------------------\n")
			file.write("\n")
	else:
		pass
file.close()
