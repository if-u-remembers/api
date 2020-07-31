import json
import requests


def put_api(api_url, yangConfig):
    requests.packages.urllib3.disable_warnings()
    headers = {"Accept": "application/yang-data+json",
               "Content-type": "application/yang-data+json"}
    # basicauth = ("developer", "C1sco12345")
    basicauth = ("cisco", "cisco123!")
    try:
        resp = requests.put(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
        if (resp.status_code >= 200 and resp.status_code <= 299):
            return '{}'.format(resp.status_code)
        else:
            # 传递错误
            return '{}'.format(resp.status_code)
    except:
        # 超时
        return '{}'.format(resp.status_code)
        # return '414'



