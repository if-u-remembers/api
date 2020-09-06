import json
import requests
import urllib3

'''
    这个class文件是为了进行api端口的调用
    传入的数据格式是 reapis(url , user , pwd) 三个命名格式，以对应不同的用户及服务器，以及api链接。
'''


class reapis:
    def __init__(self, url, user, pwd):
        self.url = url
        self.basicauth = (user, pwd)
        self.headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}

    def putapi(self, yangConfig):
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            resp = requests.put(self.url, data=json.dumps(yangConfig), auth=self.basicauth, headers=self.headers, verify=False)
            return '{}'.format(resp.status_code)
        except:
            return '400'

    def __getapi(self):
        """
        调用未配置好的数据
            :return: 返回一个get值
        """
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(self.url, auth=self.basicauth, headers=self.headers, verify=False)
        response_json = json.dumps(resp.json(), indent=4)
        return response_json

    def requestapi(self, headers, body):
        '''request方法'''
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.request("POST", self.url, headers = headers, json=body)
        return resp

    def getapi(self, headers):
        '''get方法'''
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.request("GET", self.url, headers=headers)
        return resp

    def postapi(self, headers):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.request("POST", self.url, headers=headers)
        return resp

    def getapi_to_func_one(self):
        res = self.__getapi()
        dic = json.loads(res)
        if 'errors' in dic:
            error = {"ietf-interfaces:interfaces": {"interface": [{"name": None, "description": None, "type": None, "enabled": False, "ietf-ip:ipv4": None, "ietf-ip:ipv6": None}]}}
            return error
        else:
            return json.loads(res)

    def getapis(self):
        '''调用接口'''
        return self.__getapi()
