# from pprint import pprint
import requests
import json
import sys
# import os
import myVault
# import myModules
try:
    from flask import Flask
    from flask import request
except ImportError as e:
    print(e)
    print("Looks like 'flask' library is missing.\n"
          "Type 'pip3 install flask' command to install the missing library.")
    sys.exit()

requests.packages.urllib3.disable_warnings()

runMode = input("Enter 1 for DNACenter bot or 2 for SandBoxDNA bot :")

if runMode == "1":
    bearer = myVault.botDNACenter()
elif runMode == "2":
    bearer = myVault.botSandBoxDNACenter()
else:
    print("Not valid choice!")
    sys.exit()

headers = {"Accept": "application/json", "Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + bearer}

controller_ip = "https://dnac1.cisco.com"

expected_messages = {"help me": "help",
                     "need help": "help",
                     "can you help me": "help",
                     "ayuda me": "help",
                     "help": "help",
                     "greetings": "greetings",
                     "hello": "greetings",
                     "hi": "greetings",
                     "how are you": "greetings",
                     "what's up": "greetings",
                     "what's up doc": "greetings"}


def send_spark_get(url, payload=None, js=True):
    if payload is None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js is True:
        request = request.json()
    return request


def send_spark_post(url, data):
    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request


def help_me():
    return "Sure! I can help. Below are the commands that I understand:<br/>" \
           "`Help me` - I will display what I can do.<br/>" \
           "`Hello` - I will display my greeting message<br/>" \
           "`device type switch` - I will display all the switches in the inventory<br/>" \
           "`device type router` - I will display all the routers in the inventory<br/>" \
           "`device type access point` - I will display all the access points in the inventory<br/>" \
           "`device ip x.x.x.x` - I will display the device details that match that IP Address<br/>" \
           "`device serial xyx` - I will display the device details that match that serial number<br/>" \
           "`device count` - I will display the total amount of devices managed<br/>" \
           "`host count` - I will display the total amount of hosts connected to the network<br/>"


def greetings():
    return "Hi my name is {}.<br/>" \
           "I'm currently integrated with {} <br/>" \
           "Type `Help me` to see what I can do.<br/>".format(controller_ip, bot_name)


def dnacAuth():
    resource_path = "/api/system/v1/auth/login"
    controller_login = myVault.dnacLogin(controller_ip)

    # Header information
    headers = {"content-type": "application/json", 'Authorization': controller_login}

    # Combine controller ip and api_call variables into one variable call url
    url = controller_ip + resource_path

    # login request
    response = requests.get(url, headers=headers, verify=False)
    cookie_header = {}
    cookie_header["Cookie"] = response.headers['set-cookie']
    headers.update(cookie_header)
    return headers


def dnacGET(endURL):
    url = controller_ip + "/api/v1" + endURL   # API base url
    header = dnacAuth()
    resp = requests.get(url, headers=header, verify=False)
    response_json = resp.json()
    return response_json


def dnacDeviceInfo(response_json):
    msg = ""
    msg = msg + "The hostname is : " + response_json["response"]["hostname"] + "  \n"
    msg = msg + "The IP Address : " + response_json["response"]["managementIpAddress"] + "  \n"
    msg = msg + "The device type is : " + response_json["response"]["type"] + "  \n"
    msg = msg + "The platform is : " + response_json["response"]["platformId"] + "  \n"
    msg = msg + "The serial is : " + response_json["response"]["serialNumber"] + "  \n"
    if response_json["response"]["softwareType"] is None:
        msg = msg + "The software is : " + response_json["response"]["softwareVersion"] + "  \n"

    else:
        msg = msg + "The software is : " + response_json["response"]["softwareType"] + " | " + response_json["response"]["softwareVersion"] + "  \n"

    msg = msg + "The DNAC device ID is : " + response_json["response"]["id"] + "  \n"
    msg = msg + "  \n"
    return msg


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def spark_webhook():
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        # print(json.dumps(webhook, indent=4))
        if (webhook['resource'] == "memberships") and (webhook['event'] == "created") and (webhook['data']['personEmail'] == bot_email):
            msg = ""
            msg = greetings()
            send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg})

        elif ("@webex.bot" not in webhook['data']['personEmail']) and (webhook['resource'] == "messages"):
            result = send_spark_get('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '').lower()
            in_message = in_message.replace(bot_name.lower() + " ", '')
            msg = ""

            if in_message in expected_messages and expected_messages[in_message] is "help":
                msg = help_me()

            elif in_message in expected_messages and expected_messages[in_message] is "greetings":
                msg = greetings()

            elif in_message.startswith("device type"):

                if (in_message == "device type switch") or (in_message == "device type router") or (in_message == "device type access point"):
                    message = in_message.split('device type ')[1]
                    deviceType = "{0}".format(message)

                    endURL = "/network-device"   # API base url
                    response_json = dnacGET(endURL)

                    for f in response_json["response"]:
                        typelower = f["type"].lower()
                        if deviceType in typelower:
                            msg = msg + f["platformId"] + " | " + f["serialNumber"] + " | " + f["hostname"] + " | " + f["managementIpAddress"] + "  \n"

                else:
                    msg = "I did not get that. Sorry!"

            elif in_message.startswith("device ip"):
                message = in_message.split(' ')[2]
                endURL = "/network-device/ip-address/" + message   # API base url
                response_json = dnacGET(endURL)
                msg = dnacDeviceInfo(response_json)

            elif in_message.startswith("device serial"):
                message = in_message.split(' ')[2].upper()
                endURL = "/network-device/serial-number/" + message   # API base url
                response_json = dnacGET(endURL)
                msg = dnacDeviceInfo(response_json)

            elif in_message.startswith("device count"):
                endURL = "/network-device/count"
                response_json = dnacGET(endURL)
                msg = "Total devices : " + str(response_json['response'])

            elif in_message.startswith("host count"):
                endURL = "/host/count"
                response_json = dnacGET(endURL)
                msg = "Total hosts : " + str(response_json['response'])

            else:
                msg = "Sorry, but I did not understand your request. Type `Help me` to see what I can do"

            if msg is not None:
                send_spark_post("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": msg})

        return "true"
    elif request.method == 'GET':
        message = "<center><img src=\"https://cdn-images-1.medium.com/max/800/1*wrYQF1qZ3GePyrVn-Sp0UQ.png\" alt=\"Spark Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Don't forget to create Webhooks to start receiving events from Cisco Spark!</i></b></center>" % bot_name
        return message


def main():
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_spark_get("https://api.ciscospark.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like the provided access token is not correct.\n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.ciscospark.com/apps.html "
                  "URL and generate a new access token.")
            sys.exit()
        if test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName", "")
            bot_email = test_auth.get("emails", "")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token.")
        sys.exit()

    if "@webex.bot" not in bot_email:
        print("You have provided an access token which does not relate to a Bot Account.\n"
              "Please change for a Bot Account access toekneview it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.ciscospark.com/apps.html "
              "URL and generate a new access token for your Bot.")
        sys.exit()
    else:
        app.run(host='localhost', port=8080)


if __name__ == "__main__":
    main()
