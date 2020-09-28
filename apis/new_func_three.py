from apis import reApi, mysql
import requests
import urllib3
from apis import demo
import json
import time
from requests.auth import HTTPBasicAuth


class func_three:
    def __init__(self, user, pwd, host, username, password, database):
        # 思科的
        self.urls = 'https://sandboxdnac2.cisco.com/dna/intent/api/v1/network-health'
        self.basicauth = (user, pwd)
        self.user = user
        self.pwd = pwd

        # 数据库的
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.mysql = mysql.intomysql(host=self.host, user=self.username, password=self.password, database=self.database)
        self.inmysql = mysql.inmysql(host=self.host, user=self.username, password=self.password, database=self.database)

    def __get_token(self):
        # 获取token字符串用的
        '''
        获取token串
        :return: 一个token串
        '''
        url = self.urls + '/dna/system/api/v1/auth/token'
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # try:
        token = requests.post(url, auth=HTTPBasicAuth(self.user, self.pwd),
                              headers={'content-type': 'application/json'}, verify=False).json()
        if 'error' in token:
            print('用户或者用户密码错误')
            return None
        elif 'Token' in token:
            return token['Token']

    def __get_data(self):
        # token = self.__get_token()
        # headers = {
        #     'X-Auth-Token': token,
        #     'Content-Type': "application/json",
        #     'cache-control': "no-cache"
        # }
        # resp = reApi.reapis(self.urls, self.user, self.pwd).getapi(headers)
        # data = json.loads(resp.text.encode('utf8'))
        # print(data)
        # if 200 <= resp.status_code <= 299 and data:
        #     return data
        # else:
        #     return None

        # headers = {"Accept": "application/yang-data+json", "Content-type": "application/yang-data+json"}
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # resp = requests.get(self.urls, auth=self.basicauth, headers=headers, verify=False)
        # response_json = json.dumps(resp.json(), indent=4)
        # return response_json
        return demo.data

    def data_processing(self):
        """
        :return:
        正常情况下返回: {'data': [{'name': 'oll', 'score': 100}, {'name': 'Access', 'score': 100}, {'name': 'WLC', 'score': 100}, {'name': 'AP', 'score': 100}], 'time': '2020-09-28 16:26:43'}
        不正常情况下返回: {"data": null, "time": "2020-09-28 16:28:30"}
        """
        try:
            # data = json.loads(self.__get_data())
            new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data = self.__get_data()
            if 'message' in data:
                print('进入异常处理，正常无法读取异常')
                redict = {'data': None, 'time': new_time, 'cisco_data': None}
                return json.dumps(redict)
            else:
                healthDistirubution = data['healthDistirubution']
                health_data = [{'name': 'oll', 'score': data['latestHealthScore']}]
                # 总体的
                for item in healthDistirubution:
                    # 三个其他的分布健康度数据
                    three_health = {'name': item['category'], 'score': item['healthScore']}
                    health_data.append(three_health)
                redict = {'data': health_data, 'time': new_time,  'cisco_data': healthDistirubution}
                return redict
        except TypeError:
            new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('格式异常')
            print('进入异常处理')
            redict = {'data': None, 'time': new_time, 'cisco_data': None}
            return json.dumps(redict)

    def sql_Operation_into_mysql(self):
        # 把新数据存进数据库
        data = self.data_processing()
        sql_time = data['time']
        sql_data = data['data']
        sql_name_list = ['time', 'data']
        val = ((sql_time, str(sql_data)),)
        self.mysql.add_data(val, 'health', sql_name_list)
        return data

    def redata(self):
        # 把数据发给前端
        new_data = self.sql_Operation_into_mysql()['cisco_data']
        # 获取整表
        sql_data = self.inmysql.select('health')
        new_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        re_sql_list = []
        lens = len(sql_data)
        print(lens)
        for item in sql_data:
            # 把str转list
            try:
                score_data = eval(item[2])
            # 整体的score
                score = score_data[0]['score']
                children_score = [score_data[1], score_data[2], score_data[3]]
            except:
                # 若存在异常数据，则返回空
                score = None
                children_score = []
            re_sql_dict = {'time': item[1], 'OllScore': score, 'ChildrenScore': children_score}
            re_sql_list.append(re_sql_dict)
        redata = {'time': new_time, 'CiscoData': new_data, 'data': re_sql_list}
        return redata


# host = 'li-say.top'
# mysqluser = 'root'
# password = '981002'
# database = 'office'
# func_three('admin', 'Cisco1234!', host, mysqluser, password, database).redata()
# print(func_three('admin', 'Cisco1234!', host, mysqluser, password, database).data_processing())

# # print(func_three('admin', 'Cisco1234!', host, mysqluser, password, database).sql_Operation_into_mysql())
# func_three('admin', 'Cisco1234!', host, mysqluser, password, database).sql_Operation_select_mysql()





