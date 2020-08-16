from apis import mysql, reApi
import json
from netmiko import ConnectHandler
import time


class ApiFuncThree:
    def __init__(self, host, port, user, pwd, mysqluser, password, database):
        '''
        :param host: 域名
        :param port: 端口号
        :param user: 接口用户名
        :param pwd:  接口密码
        :param mysqluser:  数据库用户名
        :param password:   数据库密码
        :param database:   数据库
        '''
        self.api_url = 'https://' + host + ':' + str(port)
        self.mysql = mysql.inmysql(host, mysqluser, password, database)
        self.url = host
        self.port = port
        self.user = user
        self.pwd = pwd

    def acl(self,  name):
        '''
        传入的url是算域名和接口号
        :param name: 接口名
        :return:
        '''
        sshCli = ConnectHandler(
            device_type='cisco_ios',
            host='www.' + self.url,
            port=self.port,
            username=self.user,
            password=self.pwd
        )
        print("configure ACL to interface.")
        config_commands = [
            'int Loopback1',
            'ip access-group 101 in'
        ]
        config_commands[0] = 'int ' + name
        print("Sending the config commands.")
        output = sshCli.send_config_set(config_commands)
        print("Config output from the device:\n{}\n".format(output))
        return output

    def down(self, user, pwd, name):
        api_url = self.api_url + '/restconf/data/ietf-interfaces:interfaces/interface=' + name
        # 需要输入url 用户及密码等
        yangConfig = {"ietf-interfaces:interface": {
            "name": "GigabitEthernet2",
            "description": "Network Interface",
            "type": "iana-if-type:ethernetCsmacd",
            "enabled": False,
            "ietf-ip:ipv4": {},
            "ietf-ip:ipv6": {}
        }}
        yangConfig['ietf-interfaces:interface']['name'] = name
        return reApi.reapis(api_url, user, pwd).putapi(yangConfig)

    def select_ddos(self):
        data = self.mysql.select('model_data')
        return data

    def GetDdosNewData(self):
        # print(self.api_url)
        api = self.api_url + '/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/'
        try:
            # 获取到所有的数据，这个接口数据为一个包含速率的数据
            data = json.loads(reApi.reapis(api, self.user, self.pwd).getapis())
            # 载入当前时间
            listtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            # 查到每个设备的参数
            list = data['Cisco-IOS-XE-interfaces-oper:interfaces']['interface']
            '''
                把新数据获取到=》载入新时间=》放到数据库内
                把旧数据提取=》 获取旧时间
                载入算法方法 =》 得到分析报告
            '''
            return json.dumps(list)
        except:
            return 0


# host = 'li-say.top'
# mysqluser = 'root'
# password = '981002'
# database = 'office'
# user = "cisco"
# pwd = "cisco123!"
# port = 6002
#
# a = ApiFuncThree(host=host, port=port, user=user, pwd=pwd, mysqluser=mysqluser, password=password, database=database)
# for i in a.select_ddos():
#     print(i)
# print(a.GetDdosNewData())

