import requests   # We use Python "requests" module to do HTTP GET query
# import myModules
import myVault


requests.packages.urllib3.disable_warnings()

error = {"errorcode": [
    {
        "Code": 200,
        "Description": "OK"
    },
    {
        "Code": 400,
        "Description": "The request was invalid or cannot be otherwise served. An accompanying error message will explain further."
    },
    {
        "Code": 401,
        "Description": "Authentication credentials were missing or incorrect."
    },
    {
        "Code": 403,
        "Description": "The request is understood, but it has been refused or access is not allowed."
    },
    {
        "Code": 404,
        "Description": "The URI requested is invalid or the resource requested, such as a user, does not exist. Also returned when the requested format is not supported by the requested method."
    },
    {
        "Code": 409,
        "Description": "The request could not be processed because it conflicts with some established rule of the system. For example, a person may not be added to a room more than once."
    },
    {
        "Code": 429,
        "Description": "Too many requests have been sent in a given amount of time and the request has been rate limited. A Retry-After header should be present that specifies how many seconds you need to wait before a successful request can be made."
    },
    {
        "Code": 500,
        "Description": "Something went wrong on the server."
    },
    {
        "Code": 503,
        "Description": "Server is overloaded with requests. Try again later."
    }
]
}


def errorCode(value):
    for f in error["errorcode"]:
        if f["Code"] == value:
            return(f["Description"])


def spaceInfo(title):
    myticket = "Bearer " + myVault.wbxTeamsToken()

    CONTROLLER_IP = "api.ciscospark.com"
    endURL = "/v1/rooms"   # API base url
    param = "?max=1000"

    url = "https://" + CONTROLLER_IP + endURL + param   # API base url

    header = {"Authorization": myticket, "content-type": "application/json"}

    resp = requests.get(url, headers=header)

    response_json = resp.json()  # Get the json-encoded content from response
    for f in response_json["items"]:
        if title in f["title"]:
            print("The space name is : ", f["title"])
            print("The roomId is : ", f["id"])
            print()


def displayName(id):
    myticket = "Bearer " + myVault.wbxTeamsToken()

    CONTROLLER_IP = "api.ciscospark.com"
    endURL = "/v1/people/"   # API base url

    url = "https://" + CONTROLLER_IP + endURL + id

    header = {"Authorization": myticket, "content-type": "application/json"}

    resp = requests.get(url, headers=header)

    response_json = resp.json()  # Get the json-encoded content from response
    return response_json["displayName"]


def name(teamId):
    myticket = "Bearer " + myVault.wbxTeamsToken()

    CONTROLLER_IP = "api.ciscospark.com"
    endURL = "/v1/teams/"   # API base url

    url = "https://" + CONTROLLER_IP + endURL + teamId

    header = {"Authorization": myticket, "content-type": "application/json"}

    resp = requests.get(url, headers=header)

    response_json = resp.json()  # Get the json-encoded content from response
    return response_json["name"]
