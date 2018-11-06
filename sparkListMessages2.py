import requests   # We use Python "requests" module to do HTTP GET query
# import json       # Import JSON encoder and decode module
# import myModules
import myVault
from ciscosparkapi import CiscoSparkAPI
api = CiscoSparkAPI(access_token=myVault.wbxTeamsToken())

requests.packages.urllib3.disable_warnings()

roomId = input("What is the room ID : ")
filename = input("What is the filename : ")

messages = api.messages.list(roomId)
messagesListed = list(messages)
members = api.memberships.list(roomId)
membersListed = list(members)
number = 0
file = open(filename, "w")

for f in reversed(messagesListed):
	try:
		if f.text != "":
			for i in membersListed:
				if i.personEmail == f.personEmail:
					displayName = i.personDisplayName
					break
			file.write(displayName + " (" + f.personEmail + ") " + f.created + "\n")
			# file.write(f.personEmail + " " + f.created + "\n")
			file.write(f.text + "\n")
			file.write("\n")
			file.write("----------------------------------------------------------------------\n")
			file.write("\n")
			number = number + 1
	except TypeError:
		pass
print("Amount of messages : " + str(number))
file.close()
