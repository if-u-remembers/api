import requests, urllib3
from requests.auth import HTTPBasicAuth

url1 = 'https://sandboxdnac2.cisco.com/dna/system/api/v1/auth/token'
Username = 'admin'
Password = 'Cisco1234!'


def get_token(myusername,mypassword):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    token = requests.post(url1, auth=HTTPBasicAuth(myusername,mypassword),
                          headers={'content-type':'application/json'},
                          verify=False,
                          )
    data1 = token.json()
    return data1['Token']

def new_project():
    ticket = get_token(Username, Password)
    url = "https://sandboxdnac2.cisco.com/dna/intent/api/v1/template-programmer/project"
    headers = {
        'X-Auth-Token':ticket,
        'Content-Type': "application/json",
        'cache-control': "no-cache"
    }
    PAYLOADF = {
        "name": "Arr100"
    }
    resp = requests.request("POST", url, headers=headers, json=PAYLOADF)
    if (resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
    else:
        print("Error code {}, reply: {}".format(resp.status_code, resp.json()))

    print(resp.text.encode('utf8'))
    return resp.json()
new_project()
